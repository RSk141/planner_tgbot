from typing import Union
from aiogram import types

from keyboards.default.menu import main_menu
from keyboards.inline.inline_tasks import settings_kb, lang
from utils.db_api import db_func as db
from localization import _


async def settings(message: Union[types.Message, types.CallbackQuery]):
    kb = await settings_kb(message.from_user.id)
    await message.answer(_('Выберите опцию'), reply_markup=kb)


async def change_notif(call: types.CallbackQuery):
    await db.change_notif(call.from_user.id)
    change = await db.get_notif(call.from_user.id)
    if change:
        await call.answer(_('Уведомления включены!'))
    else:
        await call.answer(_('Уведомления выключены!'))
    await call.message.edit_reply_markup(await settings_kb(call.from_user.id))


async def choose_language(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.edit_text(_('Выберите язык'), reply_markup=await lang(call.from_user.id))


async def change_lang(call: types.CallbackQuery, callback_data: dict):
    lang = callback_data.get('lang')
    await db.change_lang(call.from_user.id, lang)
    await call.message.delete()
    await call.message.answer(_('Язык успешно именен!', locale=lang), reply_markup=await main_menu(lang))
