from aiogram import Dispatcher

from handlers.errors.error_handler import errors_handler


def setup(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
