from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.inline_tasks import change_tasks_kb, choose_task_kb
from states import states
from utils.db_api import db_func as db

from keyboards.inline.inline_tasks import cancel_kb
from localization import _


async def show_plans(message: types.Message):
    today = datetime.today().weekday()
    tasks = await db.get_tasks(message.from_user.id, today)
    t = []
    t_done = []
    for task_id, task, done in tasks:
        if done:
            t_done.append(f'✅ {task}')
        else:
            t.append(f'🚫 {task}')

    if len(t_done) != 0:
        done_tasks = _("\n\n<b>Выполненные задачи:</b>\n") + "\n".join(t_done)
    else:
        done_tasks = ''

    await message.answer(_("<b>Ваши планы на сегодня:</b>\n") + "\n".join(t) + done_tasks,
                         reply_markup=await change_tasks_kb(today))


async def start_adding_task(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    day = callback_data.get('day')
    await call.message.answer(_('Пожалуйста, введите новую задачу..'), reply_markup=await cancel_kb())
    await states.Task.add_task.set()
    await state.update_data(user_id=call.from_user.id, day=day)


async def add_task(message: types.Message, state: FSMContext):
    await state.update_data(task=message.text)
    async with state.proxy() as data:
        user_id = data.get('user_id')
        task = data.get('task')
        day = int(data.get('day'))

    await state.finish()
    await db.add_task(user_id, task, day)
    await message.answer(_('Задача успешно добавлена!'))


async def choose_done(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    day = int(callback_data.get('day'))
    await call.message.answer(_('Пожалуйста, выберите выполненное задание'),
                              reply_markup=await choose_task_kb(call.from_user.id, 'done', day))


async def mark_done(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    task_id = int(callback_data.get('task_id'))
    await db.mark_done(task_id)
    await call.message.answer(_('Задание отмечено как выполненное!'))


async def choose_del(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    day = int(callback_data.get('day'))
    await call.message.answer(_('Пожалуйста выберите задание, которое хотите удалить'),
                              reply_markup=await choose_task_kb(call.from_user.id, 'delete', day))


async def delete_task(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    task_id = int(callback_data.get('task_id'))
    await db.delete_task(task_id)
    await call.message.answer(_('Задание удалено!'))


async def choose_edit(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    day = int(callback_data.get('day'))
    await call.message.answer(_('Пожалуйста выберите задание, которое хотите редактировать'),
                              reply_markup=await choose_task_kb(call.from_user.id, 'edit', day))


async def start_editing(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    task_id = int(callback_data.get('task_id'))
    task = await db.get_task(task_id)
    await call.message.answer(_('Вы собираетесь изменить задание:\n<i>{task}</i>\n'
                                'Пожалуйста введите изменнённое задание').format(task=task))
    await states.Task.edit_task.set()
    await state.update_data(task_id=task_id)


async def edit_task(message: types.Message, state: FSMContext):
    await state.update_data(task=message.text)
    async with state.proxy() as data:
        task_id = data.get('task_id')
        task = data.get('task')
    await state.finish()
    await db.edit_task(task_id, task)
    await message.answer(_('Задание успешно изменено'))
