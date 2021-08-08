from typing import Union
from aiogram import types

from bot.keyboards.default.menu import main_menu
from bot.keyboards.inline.inline_tasks import settings_kb, lang
from utils.db_api import db_func as db
from bot.reqi import _


async def settings(message: Union[types.Message, types.CallbackQuery]):
    kb = await settings_kb(message.from_user.id)
    text = _('Выберите опцию')
    if isinstance(message, types.Message):
        await message.answer(text, reply_markup=kb)
    if isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(text, reply_markup=kb)


async def change_notif(call: types.CallbackQuery):
    await db.change_notif(call.from_user.id)
    change = await db.get_notif(call.from_user.id)
    if change:
        await call.answer(_('Уведомления включены!'))
    else:
        await call.answer(_('Уведомления выключены!'))
    await call.message.edit_reply_markup(await settings_kb(call.from_user.id))


async def choose_language(call: types.CallbackQuery):
    markup = await lang(call.from_user.id)
    await call.message.edit_text(_('Выберите язык'), reply_markup=markup)


async def change_lang(call: types.CallbackQuery):
    lang = call.data[-2:]
    await db.change_lang(call.from_user.id, lang)
    await call.message.delete()
    await call.message.answer(_('Язык успешно именен!'), reply_markup=await main_menu(lang))
