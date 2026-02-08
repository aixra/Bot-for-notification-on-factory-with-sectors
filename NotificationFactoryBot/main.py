import asyncio
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

TOKEN = "" #Token of your BOT

init_db() #Function of initialization, which write in sql.py

class Form(StatesGroup):
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
        await message.answer("Выберите сектор:", reply_markup=kb.main)

    @dp.message(StateFilter(None), F.text) #
    async def sector_chosen(message: Message, state: FSMContext):
        if message.text.startswith(config.SECTOR_PREFIX):
            sector = int(message.text.split(" ")[1])
            await state.update_data(sector=sector)
            await state.set_state(Form.waiting_for_note)
            await message.answer(f"Напишите заметку для сектора {sector}")
        elif message.text.startswith(config.BACK_BUTTON): #Button Back
            await state.clear()
            await message.answer("Выберите сектор:", reply_markup=kb.main)

    #Shield from non text message
    @dp.message(~F.text)
    async def not_text(message: Message):
        await message.answer("❌ Пожалуйста, отправьте текстовое сообщение")

    @dp.message(StateFilter(Form.waiting_for_note), F.text) #After you choose the sector it starts work
    async def save_note(message: Message, state: FSMContext):
        if(message.text.startswith(config.BACK_BUTTON)):
            await state.clear()
            await message.answer("Выберите сектор:", reply_markup=kb.main)
            return
        if (message.text.startswith(config.SECTOR_PREFIX)):
            await message.answer("Сначала допишите заметку.", reply_markup=kb.main)
            return
        data = await state.get_data()
        sector = data.get("sector")
        note = message.text
        print(note, sector)
        save_message(message.from_user.id, sector, note)
        await state.clear()
        await message.answer(f"Заметка сохранена: {note}", reply_markup=kb.main)

        #ADMIN NOTIFICATION
        ADMIN_ID = config.ADMIN_CHAT_ID #Сюда указываем ID чата или тг аккаунта которая можно узнать написав "/id" в чате
        user = message.from_user
        user_mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        await bot.send_message(
            ADMIN_ID,
            f"🆕 Новая заметка\n"
            f"Пользователь: {user_mention}\n"
            f"Сектор: {sector}\n"
            f"Текст: {note}",
            parse_mode = "HTML"
        )


    await dp.start_polling(bot)

asyncio.run(main())
