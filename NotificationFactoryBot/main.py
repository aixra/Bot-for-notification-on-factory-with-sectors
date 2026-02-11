import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F

#impotrt config
import config

#Button inicializtion
import keyBoardReply as kb

#SQL inicialization
from sql import init_db, save_message, get_all_message
from google_tables import append_complaint_to_google_tables, build_request_id


TOKEN = "" #Token of your BOT

init_db() #Function of initialization, which write in sql.py


class Form(StatesGroup):
    waiting_for_name = State()
    waiting_for_sector = State()
    waiting_for_device = State()
    waiting_for_note = State()


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    #Id detector
    @dp.message(Command("id"))
    async def get_id(message: Message):
        await message.answer(
            f"👤 Ваш ID: {message.from_user.id}\n"
            f"💬 ID чата: {message.chat.id}"
        )

    #Main Code
    @dp.message(Command("start")) #/start
    async def start(message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(Form.waiting_for_name)
        name = message.text
        await message.answer("Как вас называть?")

    #Save user name
    @dp.message(StateFilter(Form.waiting_for_name), F.text)
    async def get_name(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(Form.waiting_for_sector)
        await message.answer("Выберите сектор:", reply_markup=kb.main)

    #Sector choose
    @dp.message(StateFilter(Form.waiting_for_sector), F.text)
    async def sector_chosen(message: Message, state: FSMContext):
        if not message.text.startswith(config.SECTOR_PREFIX):
            await message.answer("❌ Пожалуйста, выберите сектор кнопкой", reply_markup=kb.main)
            return

        data = await state.get_data()
        if not data.get("request_started_at"):
            await state.update_data(request_started_at=message.date.isoformat())

        sector = int(message.text.split(" ")[1])
        await state.update_data(sector=sector)
        await state.set_state(Form.waiting_for_device)
        await message.answer(
            f"Выберите станок из сектора {sector}:",
            reply_markup=kb.deviceChoose
        )

    #Device choose
    @dp.message(StateFilter(Form.waiting_for_device), F.text)
    async def device_chosen(message: Message, state: FSMContext):
        if message.text.startswith(config.BACK_BUTTON1): #Button Back
            await state.set_state(Form.waiting_for_sector)
            await message.answer("Выберите сектор:", reply_markup=kb.main)
            return

        if not message.text.startswith(config.DEVICE_PREFIC):
            await message.answer("❌ Выберите станок кнопкой", reply_markup=kb.deviceChoose)
            return

        device = int(message.text.split(" ")[1])
        await state.update_data(device=device)
        await state.set_state(Form.waiting_for_note)
        await message.answer(
            "Напишите заметку:",
            reply_markup=kb.Back
        )

    #Save note
    @dp.message(StateFilter(Form.waiting_for_note), F.text)
    async def save_note(message: Message, state: FSMContext):
        if message.text.startswith(config.BACK_BUTTON1):
            await state.set_state(Form.waiting_for_device)
            await message.answer("Выберите станок:", reply_markup=kb.deviceChoose)
            return

        if message.text.startswith(config.SECTOR_PREFIX):
            await message.answer("❌ Сначала допишите заметку", reply_markup=kb.Back)
            return

        if len(message.text.strip()) < 5:
            await message.answer("Введите текст жалобы", reply_markup=kb.Back)
            return

        data = await state.get_data()
        sector = data.get("sector")
        device = data.get("device")
        note = message.text
        request_started_at = data.get("request_started_at")
        request_time = datetime.fromisoformat(request_started_at) if request_started_at else message.date

        print(note, sector, device)

        await message.answer(
            f"Заметка сохранена для участка {sector} и станка {device}:\n{note}",
        )
        await state.set_state(Form.waiting_for_sector) #!!!!
        await message.answer(
            f"Выберите сектор:\n",
            reply_markup=kb.main
        )


        #ADMIN NOTIFICATION
        ADMIN_ID = config.ADMIN_CHAT_ID #Сюда указываем ID чата или тг аккаунта
        user = message.from_user
        if user.username:
            user_text = f"@{user.username}"
        else:
            user_text = user.first_name
        data = await state.get_data()
        name = data.get("name")
        await bot.send_message(
            ADMIN_ID,
            f"🆕 Новая заметка\n"
            f"Пользователь: {user_text}\n"
            f"Имя: {name}\n"
            f"Сектор: {sector}\n"
            f"Станок: {device}\n"
            f"Текст: {note}",
            parse_mode="HTML"
        )

        append_complaint_to_google_tables(
            spreadsheet_id=config.GOOGLE_TABLES_SPREADSHEET_ID,
            credentials_path=config.GOOGLE_TABLES_CREDENTIALS_FILE,
            sheet_name=config.GOOGLE_TABLES_SHEET_NAME,
            request_id=build_request_id(message.from_user.id, request_time),
            request_time=request_time,
            user_name=name or user_text,
            sector=sector,
            device=device,
            complaint_text=note,
        )
        await state.update_data(request_started_at=None)

        #Save photo

    @dp.message(StateFilter(Form.waiting_for_note), F.photo)
    async def save_note_photo(message: Message, state: FSMContext):
        data = await state.get_data()
        sector = data.get("sector")
        device = data.get("device")
        request_started_at = data.get("request_started_at")
        request_time = datetime.fromisoformat(request_started_at) if request_started_at else message.date

        photo_id = message.photo[-1].file_id
        note = message.caption if message.caption else "(без текста)"

        print(note, sector, device, photo_id)
        # save_message(message.from_user.id, sector, device, note)

        await message.answer(
            f"Заметка с фото сохранена для участка {sector} и станка {device}",
        )
        await state.set_state(Form.waiting_for_sector)
        await message.answer("Выберите сектор:", reply_markup=kb.main)

        # ADMIN
        ADMIN_ID = config.ADMIN_CHAT_ID
        user = message.from_user
        user_text = f"@{user.username}" if user.username else user.first_name
        name = data.get("name")

        await bot.send_photo(
            ADMIN_ID,
            photo=photo_id,
            caption=
            f"🆕 Новая заметка\n"
            f"Пользователь: {user_text}\n"
            f"Имя: {name}\n"
            f"Сектор: {sector}\n"
            f"Станок: {device}\n"
            f"Текст: {note}",
        )

        append_complaint_to_google_tables(
            spreadsheet_id=config.GOOGLE_TABLES_SPREADSHEET_ID,
            credentials_path=config.GOOGLE_TABLES_CREDENTIALS_FILE,
            sheet_name=config.GOOGLE_TABLES_SHEET_NAME,
            request_id=build_request_id(message.from_user.id, request_time),
            request_time=request_time,
            user_name=name or user_text,
            sector=sector,
            device=device,
            complaint_text=note,
        )
        await state.update_data(request_started_at=None)

    # Shield from non text message
    @dp.message(~F.text & ~F.photo)
    async def not_supported(message: Message):
        await message.answer("❌ Поддерживаются только текст и фото")
    await dp.start_polling(bot)


asyncio.run(main())
