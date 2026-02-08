from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import CallbackQuery

import config

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=config.SECTOR1), KeyboardButton(text=config.SECTOR2)],
        [KeyboardButton(text=config.SECTOR3), KeyboardButton(text=config.SECTOR4)],
        [KeyboardButton(text=config.BACK_BUTTON)],
    ],
    resize_keyboard=True,      # компактные кнопки
    one_time_keyboard=False
)