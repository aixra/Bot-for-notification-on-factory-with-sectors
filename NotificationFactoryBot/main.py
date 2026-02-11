import asyncio
from datetime import datetime
from io import BytesIO

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InputMediaPhoto, Message

import config
import keyBoardReply as kb
from catalog_loader import load_catalog
from email_sender import send_complaint_email
from google_tables import append_complaint_to_google_tables
from request_counter import get_next_request_id
from sql import get_all_message, init_db, save_message
from user_auth_loader import is_login_allowed

TOKEN = ""  # Token of your BOT

init_db()


class Form(StatesGroup):
    waiting_for_login = State()
    waiting_for_sector = State()
    waiting_for_device = State()
    waiting_for_note = State()


ALBUM_BUFFER: dict[str, dict] = {}


def build_user_name(message: Message) -> str:
    user = message.from_user
    full_name = " ".join(filter(None, [user.first_name, user.last_name]))
    if user.username:
        return f"@{user.username} ({full_name})" if full_name else f"@{user.username}"
    return full_name or str(user.id)


async def download_telegram_file(bot: Bot, file_id: str) -> bytes:
    telegram_file = await bot.get_file(file_id)
    stream = BytesIO()
    await bot.download_file(telegram_file.file_path, destination=stream)
    return stream.getvalue()


async def send_admin_notification(
    bot: Bot,
    user_text: str,
    request_id: int,
    request_time: datetime,
    sector: str,
    device: str,
    note: str,
    photo_ids: list[str],
):
    caption = (
        f"🆕 Новая заметка №{request_id}\n"
        f"Пользователь: {user_text}\n"
        f"Время: {request_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Сектор: {sector}\n"
        f"Станок: {device}\n"
        f"Текст: {note}"
    )

    if not photo_ids:
        await bot.send_message(config.ADMIN_CHAT_ID, caption)
        return

    media = [InputMediaPhoto(media=photo_ids[0], caption=caption)]
    media.extend(InputMediaPhoto(media=photo_id) for photo_id in photo_ids[1:])
    await bot.send_media_group(config.ADMIN_CHAT_ID, media=media)


async def persist_request(
    bot: Bot,
    message: Message,
    state: FSMContext,
    note: str,
    photo_ids: list[str],
):
    data = await state.get_data()
    sector = data.get("sector")
    device = data.get("device")
    user_text = data.get("user_name") or build_user_name(message)

    request_started_at = data.get("request_started_at")
    request_time = datetime.fromisoformat(request_started_at) if request_started_at else message.date
    request_id = get_next_request_id()

    await send_admin_notification(
        bot=bot,
        user_text=user_text,
        request_id=request_id,
        request_time=request_time,
        sector=sector,
        device=device,
        note=note,
        photo_ids=photo_ids,
    )

    append_complaint_to_google_tables(
        spreadsheet_id=config.GOOGLE_TABLES_SPREADSHEET_ID,
        credentials_path=config.GOOGLE_TABLES_CREDENTIALS_FILE,
        sheet_name=config.GOOGLE_TABLES_SHEET_NAME,
        request_id=request_id,
        request_time=request_time,
        user_name=user_text,
        sector=sector,
        device=device,
        complaint_text=note,
    )

    attachments: list[tuple[str, bytes]] = []
    for index, photo_id in enumerate(photo_ids, start=1):
        content = await download_telegram_file(bot, photo_id)
        attachments.append((f"complaint_{request_id}_{index}.jpg", content))

    send_complaint_email(
        request_id=request_id,
        request_time=request_time.strftime("%Y-%m-%d %H:%M:%S"),
        user_name=user_text,
        sector=sector,
        device=device,
        complaint_text=note,
        photo_attachments=attachments,
    )

    await state.update_data(request_started_at=None)
    await state.set_state(Form.waiting_for_sector)

    catalog = load_catalog()
    await message.answer("Обращение сохранено")
    await message.answer(
        "Выберите сектор:",
        reply_markup=kb.build_sectors_keyboard(list(catalog.keys())),
    )


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(Command("id"))
    async def get_id(message: Message):
        await message.answer(f"👤 Ваш ID: {message.from_user.id}\n💬 ID чата: {message.chat.id}")

    @dp.message(Command("start"))
    async def start(message: Message, state: FSMContext):
        await state.clear()
        user_name = build_user_name(message)
        await state.update_data(user_name=user_name)
        await state.set_state(Form.waiting_for_login)
        await message.answer(
            "Введите ваш логин (он должен быть в файле allowed_users.xlsx, одна строка = один пользователь Telegram):"
        )

    @dp.message(StateFilter(Form.waiting_for_login), F.text)
    async def authorize_user(message: Message, state: FSMContext):
        input_login = message.text.strip()
        if not is_login_allowed(input_login):
            await message.answer("❌ Доступ запрещен. Логин не найден в списке разрешенных пользователей.")
            return

        await state.update_data(
            authorized_login=input_login.lstrip("@"),
            request_started_at=message.date.isoformat(),
        )
        await state.set_state(Form.waiting_for_sector)
        catalog = load_catalog()
        await message.answer(
            "✅ Доступ разрешен. Выберите сектор:",
            reply_markup=kb.build_sectors_keyboard(list(catalog.keys())),
        )

    @dp.message(StateFilter(Form.waiting_for_sector), F.text)
    async def sector_chosen(message: Message, state: FSMContext):
        catalog = load_catalog()
        if message.text not in catalog:
            await message.answer(
                "❌ Пожалуйста, выберите сектор кнопкой",
                reply_markup=kb.build_sectors_keyboard(list(catalog.keys())),
            )
            return

        data = await state.get_data()
        if not data.get("request_started_at"):
            await state.update_data(request_started_at=message.date.isoformat())

        await state.update_data(sector=message.text)
        await state.set_state(Form.waiting_for_device)
        await message.answer(
            f"Выберите станок из сектора {message.text}:",
            reply_markup=kb.build_devices_keyboard(catalog[message.text]),
        )

    @dp.message(StateFilter(Form.waiting_for_device), F.text)
    async def device_chosen(message: Message, state: FSMContext):
        if message.text == config.BACK_BUTTON2:
            catalog = load_catalog()
            await state.set_state(Form.waiting_for_sector)
            await message.answer("Выберите сектор:", reply_markup=kb.build_sectors_keyboard(list(catalog.keys())))
            return

        data = await state.get_data()
        sector = data.get("sector")
        catalog = load_catalog()
        allowed_devices = catalog.get(sector, [])

        if message.text not in allowed_devices:
            await message.answer("❌ Выберите станок кнопкой", reply_markup=kb.build_devices_keyboard(allowed_devices))
            return

        await state.update_data(device=message.text)
        await state.set_state(Form.waiting_for_note)
        await message.answer("Напишите заметку или отправьте фото:", reply_markup=kb.Back)

    @dp.message(StateFilter(Form.waiting_for_note), F.text)
    async def save_note(message: Message, state: FSMContext):
        if message.text == config.BACK_BUTTON1:
            data = await state.get_data()
            sector = data.get("sector")
            catalog = load_catalog()
            await state.set_state(Form.waiting_for_device)
            await message.answer("Выберите станок:", reply_markup=kb.build_devices_keyboard(catalog.get(sector, [])))
            return

        if len(message.text.strip()) < 5:
            await message.answer("Введите текст жалобы", reply_markup=kb.Back)
            return

        await persist_request(bot, message, state, message.text, photo_ids=[])

    @dp.message(StateFilter(Form.waiting_for_note), F.photo)
    async def save_note_photo(message: Message, state: FSMContext):
        note = message.caption if message.caption else "(без текста)"

        if message.media_group_id:
            key = f"{message.chat.id}:{message.from_user.id}:{message.media_group_id}"
            entry = ALBUM_BUFFER.setdefault(key, {"photo_ids": [], "note": note, "last_ts": 0.0, "lock": asyncio.Lock()})
            async with entry["lock"]:
                entry["photo_ids"].append(message.photo[-1].file_id)
                if message.caption:
                    entry["note"] = message.caption
                entry["last_ts"] = asyncio.get_running_loop().time()

            await asyncio.sleep(1.0)
            current = ALBUM_BUFFER.get(key)
            if not current:
                return
            if asyncio.get_running_loop().time() - current["last_ts"] < 0.9:
                return

            async with current["lock"]:
                photo_ids = list(current["photo_ids"])
                note = current["note"]
                ALBUM_BUFFER.pop(key, None)

            await persist_request(bot, message, state, note, photo_ids=photo_ids)
            return

        await persist_request(bot, message, state, note, photo_ids=[message.photo[-1].file_id])

    @dp.message(~F.text & ~F.photo)
    async def not_supported(message: Message):
        await message.answer("❌ Поддерживаются только текст и фото")

    await dp.start_polling(bot)


asyncio.run(main())
