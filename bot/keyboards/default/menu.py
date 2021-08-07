from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.db_api import db_func as db


async def main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="Планы на сегодня 📝"),
            KeyboardButton(text="Планы на неделю 📝"),
        ],
        [
            KeyboardButton(text="Обратная связь 📲"),
            KeyboardButton(text="Настройки ⚙️")
        ]
    ]
    kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return kb
