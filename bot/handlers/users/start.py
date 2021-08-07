from aiogram import types

from utils.db_api import db_func as db

from keyboards.default.menu import main_menu


async def bot_start(message: types.Message):
    await message.answer("Здраствуйте 👋 Я помогу вам упорядочить ващи дела и создать удобный список задач!\n"
                         "Если возникли проблемы или вопросы, вы можете обратится в поддержку. Успехов в достижении "
                         "вашей цели! 🤗",
                         reply_markup=await main_menu())
    await db.add_user(message.from_user.id, message.from_user.username,
                      message.from_user.full_name)


async def close_menu(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
