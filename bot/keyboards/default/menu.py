from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.db_api import db_func as db
from localization import _l


async def main_menu(lang) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text=_l("Планы на сегодня 📝", locale=lang)),
            KeyboardButton(text=_l("Планы на неделю 📝", locale=lang)),
        ],
        [
            KeyboardButton(text=_l("Обратная связь 📲", locale=lang)),
            KeyboardButton(text=_l("Настройки ⚙️", locale=lang))
        ]
    ]
    kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return kb
