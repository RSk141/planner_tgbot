from pathlib import Path

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares import i18n
from aiogram.types import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.middlewares import Localization
from data import config
from utils.db_api import database
from utils.db_api.database import db
from utils.misc import scheduled_jobs
from reqi import i18n

async def on_startup(dispatcher: Dispatcher):
    import middlewares
    import filters
    import handlers

    middlewares.setup(dp)
    filters.setup(dp)
    handlers.errors.setup(dp)
    handlers.users.setup(dp)

    await database.on_startup(dp)

    await db.gino.create_all()

    scheduled_jobs.setup(scheduler, dp)


if __name__ == '__main__':
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    scheduler = AsyncIOScheduler()
    dp.middleware.setup(i18n)

    executor.start_polling(dp, on_startup=on_startup)
