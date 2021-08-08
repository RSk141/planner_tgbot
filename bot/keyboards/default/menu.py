from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.db_api import db_func as db
from bot.reqi import _


async def main_menu(lang=None) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text=_("Планы на сегодня 📝"), locale=lang),
            KeyboardButton(text=_("Планы на неделю 📝"), locale=lang),
        ],
        [
            KeyboardButton(text=_("Обратная связь 📲"), locale=lang),
            KeyboardButton(text=_("Настройки ⚙️"), locale=lang)
        ]
    ]
    kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return kb
