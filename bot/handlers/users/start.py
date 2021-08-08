from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.db_api import db_func as db

from keyboards.default.menu import main_menu
from bot.reqi import _


async def bot_start(message: types.Message):
    menu = await main_menu()
    await message.answer(_("Здраствуйте 👋 Я помогу вам упорядочить ващи дела и создать удобный список задач!\n"
                           "Если возникли проблемы или вопросы, вы можете обратится в поддержку. Успехов в достижении "
                           "вашей цели! 🤗"),
                         reply_markup=menu)
    await db.add_user(message.from_user.id, message.from_user.username,
                      message.from_user.full_name)


async def close_menu(call: types.CallbackQuery):
    await call.message.edit_reply_markup()


async def close_menu_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
