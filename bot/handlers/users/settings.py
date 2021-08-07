from aiogram import types

from keyboards.inline.inline_tasks import settings_kb
from utils.db_api import db_func as db


async def settings(message: types.Message):
    await message.answer('Выберите опцию', reply_markup=await settings_kb(message.from_user.id))


async def change_notif(call: types.CallbackQuery):
    await db.change_notif(call.from_user.id)
    change = await db.get_notif(call.from_user.id)
    if change:
        await call.answer('Уведомления включены!')
    else:
        await call.answer('Уведомления выключены!')
    await call.message.edit_reply_markup(await settings_kb(call.from_user.id))
