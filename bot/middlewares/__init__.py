from aiogram import Dispatcher

from .language_middleware import Localization
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())

