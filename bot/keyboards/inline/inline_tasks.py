from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api import db_func as db


menu_callback = CallbackData('tasks', 'name', 'day')
tasks_callback = CallbackData('done', 'name', 'task_id')
day_callback = CallbackData('week_day', 'name', 'day')
reply_support_callback = CallbackData('support', 'name', 'user_id')


async def change_tasks_kb(day: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Добавить задачу 📝", callback_data=menu_callback.new(name='add_task', day=day))
        ],
        [
            InlineKeyboardButton(text="Сделано 👌", callback_data=menu_callback.new(name='done', day=day)),
            InlineKeyboardButton(text="Редактировать ✏️", callback_data=menu_callback.new(name='edit', day=day))
        ],
        [
            InlineKeyboardButton(text="Удалить 🗑️", callback_data=menu_callback.new(name='delete', day=day)),
            InlineKeyboardButton(text="Закрыть 🚪", callback_data='close')
        ]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return kb


async def choose_task_kb(user_id: int, action: str, day: int) -> InlineKeyboardMarkup:
    tasks = await db.get_tasks(user_id, day)
    kb = InlineKeyboardMarkup()
    for task_id, task, done in tasks:
        if not done:
            kb.add(InlineKeyboardButton(text=task, callback_data=tasks_callback.new(name=f'{action}_task',
                                                                                    task_id=task_id)))
    return kb


async def week_day_kb(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    week = [{"Пн": 0}, {"Вт": 1}, {"Ср": 2}, {"Чт️": 3}, {"Пт": 4}, {"Сб": 5}, {"Вс": 6}]
    today = datetime.today().weekday()
    kb_week = week[today+1:] + week[:today]

    for week_d in kb_week:
        for day, num in week_d.items():
            tasks_count = len(await db.get_tasks(user_id, num))
            if tasks_count > 0:
                counter = f' [{tasks_count}]'
            else:
                counter = ''
            kb.insert(InlineKeyboardButton(text=day+counter, callback_data=day_callback.new(name='week_day', day=num)))

    return kb


async def confirm_support() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Да', callback_data='confirm'),
           InlineKeyboardButton(text='Нет', callback_data='close'))
    return kb


async def reply_support(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Ответить', callback_data=reply_support_callback.new(name='reply',
                                                                                          user_id=user_id)),
           InlineKeyboardButton(text='Игнорировать', callback_data='close'))
    return kb


async def settings_kb(user_id: int) -> InlineKeyboardMarkup:
    notif = await db.get_notif(user_id)
    if notif:
        btn = 'Выключить уведомления 🔕'
    else:
        btn = 'Включить уведомления 🔔'
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=btn, callback_data='change_notif')).add(InlineKeyboardButton(text='Отмена',
                                                                                                  callback_data='close'))
    return kb
