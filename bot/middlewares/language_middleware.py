from typing import Tuple, Any
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from bot.utils.db_api.database import User
from bot.utils.db_api import db_func as db


class Localization(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user = types.User.get_current()
        return await db.get_lang(user.id)



