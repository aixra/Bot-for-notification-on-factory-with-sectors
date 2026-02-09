from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import CallbackQuery

import config

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=config.SECTOR1), KeyboardButton(text=config.SECTOR2)],
        [KeyboardButton(text=config.SECTOR3), KeyboardButton(text=config.SECTOR4)],
        #[KeyboardButton(text=config.BACK_BUTTON1)],
    ],
    resize_keyboard=True,      # компактные кнопки
    one_time_keyboard=True
)
deviceChoose = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Device 1"), KeyboardButton(text="Device 2")],
        [KeyboardButton(text="Device 3"), KeyboardButton(text="Device 4")],
        [KeyboardButton(text=config.BACK_BUTTON2)],
    ],
    resize_keyboard=True,      # компактные кнопки
    one_time_keyboard=True
)
Back = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=config.BACK_BUTTON1)],
    ],
    resize_keyboard=True,      # компактные кнопки
    one_time_keyboard=True
)
