from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api import db_func as db
from localization import _, _l

menu_callback = CallbackData('tasks', 'name', 'day')
tasks_callback = CallbackData('done', 'name', 'task_id')
day_callback = CallbackData('week_day', 'name', 'day')
reply_support_callback = CallbackData('support', 'name', 'user_id')
lang_callback = CallbackData('lang', 'name', 'lang')
pagination_call = CallbackData('pagination', 'key', 'page')


async def change_tasks_kb(day: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text=_("Добавить задачу 📝"),
                                 callback_data=menu_callback.new(name='add_task', day=day))
        ],
        [
            InlineKeyboardButton(text=_("Сделано 👌"), callback_data=menu_callback.new(name='done', day=day)),
            InlineKeyboardButton(text=_("Редактировать ✏️"), callback_data=menu_callback.new(name='edit', day=day))
        ],
        [
            InlineKeyboardButton(text=_("Удалить 🗑️"), callback_data=menu_callback.new(name='delete', day=day)),
            InlineKeyboardButton(text=_("Закрыть 🚪"), callback_data='close')
        ]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return kb


async def choose_task_kb(user_id: int, day: int, action: str, page: int = 1) -> InlineKeyboardMarkup:
    tasks = await db.get_tasks(user_id, day)
    MAX_ITEMS_PER_PAGE = 3
    key = "items"
    markup = InlineKeyboardMarkup(row_width=3)
    first_item_index = (page - 1) * MAX_ITEMS_PER_PAGE
    last_item_index = page * MAX_ITEMS_PER_PAGE

    sliced_array = tasks[first_item_index:last_item_index]
    for task_id, task, done in sliced_array:
        if not done:
            markup.add(InlineKeyboardButton(text=task, callback_data=tasks_callback.new(name=f'{action}_task',
                                                                                        task_id=task_id)))

    if len(tasks) % MAX_ITEMS_PER_PAGE == 0:
        max_page = len(tasks) // MAX_ITEMS_PER_PAGE
    else:
        max_page = len(tasks) // MAX_ITEMS_PER_PAGE + 1


    pages_buttons = list()
    first_page = 1
    first_page_text = "<<"

    pages_buttons.append(
        InlineKeyboardButton(
            text=first_page_text,
            callback_data=pagination_call.new(key=key,
                                              page=first_page)
        )
    )

    previous_page = page - 1
    previous_page_text = '<<'

    if previous_page >= first_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=key,
                                                  page=previous_page)
            )
        )

    pages_buttons.append(
        InlineKeyboardButton(
            text=f"- {page} -",
            callback_data=pagination_call.new(key=key,
                                              page="current_page")
        )
    )

    next_page = page + 1
    next_page_text = '>>'

    if next_page <= max_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=key,
                                                  page=next_page)))

    if len(tasks) > 3:
        markup.row(*pages_buttons)
    markup.add(InlineKeyboardButton(text=_('Отмена'), callback_data='close'))

    return markup


async def week_day_kb(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    week = ({_("Пн"): 0}, {_("Вт"): 1}, {_("Ср"): 2}, {_("Чт️"): 3}, {_("Пт"): 4}, {_("Сб"): 5}, {_("Вс"): 6})
    today = datetime.today().weekday()
    kb_week = week[today + 1:] + week[:today]

    for week_d in kb_week:
        for day, num in week_d.items():
            tasks_count = len(await db.get_tasks(user_id, num))
            counter = f' [{tasks_count}]' if tasks_count > 0 else ''
            kb.insert(
                InlineKeyboardButton(text=day + counter, callback_data=day_callback.new(name='week_day', day=num)))

    return kb


async def confirm_support() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=_('Да'), callback_data='confirm'),
           InlineKeyboardButton(text=_('Нет'), callback_data='close'))
    return kb


async def reply_support(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=_('Ответить'), callback_data=reply_support_callback.new(name='reply',
                                                                                             user_id=user_id)),
           InlineKeyboardButton(text=_('Игнорировать'), callback_data='close'))
    return kb


async def settings_kb(user_id: int) -> InlineKeyboardMarkup:
    btn = _('Выключить уведомления 🔕') if await db.get_notif(user_id) else _('Включить уведомления 🔔')
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=btn, callback_data='change_notif')).add(
        InlineKeyboardButton(text=_('Изменить язык 🌍'), callback_data='change_language')).add(
        InlineKeyboardButton(text=_('Отмена'),
                             callback_data='close'))

    return kb


async def lang():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Українська 🇺🇦', callback_data=lang_callback.new(name='lang', lang='uk'))).add(
        InlineKeyboardButton(text='English 🇬🇧', callback_data=lang_callback.new(name='lang', lang='en'))).add(
        InlineKeyboardButton(text='Русский 🇷🇺', callback_data=lang_callback.new(name='lang', lang='ru'))).add(
        InlineKeyboardButton(text=_('Назад'), callback_data='back')
    )
    return kb


async def cancel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text=_('Отмена'), callback_data='close'))
    return kb
