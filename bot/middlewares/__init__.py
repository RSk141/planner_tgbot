from aiogram import Dispatcher

from .language_middleware import Localization
from .throttling import ThrottlingMiddleware
from data.config import I18N_DOMAIN, LOCALES_DIR


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(Localization(I18N_DOMAIN, LOCALES_DIR))

