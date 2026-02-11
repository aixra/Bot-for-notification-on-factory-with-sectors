from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

import config


def _chunk(items: list[str], size: int = 2) -> list[list[KeyboardButton]]:
    rows: list[list[KeyboardButton]] = []
    for i in range(0, len(items), size):
        rows.append([KeyboardButton(text=item) for item in items[i : i + size]])
    return rows


def build_sectors_keyboard(sectors: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=_chunk(sectors),
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_devices_keyboard(devices: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=_chunk(devices) + [[KeyboardButton(text=config.BACK_BUTTON2)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


Back = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=config.BACK_BUTTON1)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
