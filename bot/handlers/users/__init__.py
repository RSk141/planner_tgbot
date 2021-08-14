from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart

from handlers.users.start import bot_start, close_menu
from handlers.users.today_plans import show_plans, start_adding_task, add_task, choose_done, mark_done, choose_del, \
    delete_task, choose_edit, start_editing, edit_task
from handlers.users.week_plans import choose_day, show_week_plans
from handlers.users.support import call_support, support, send_to_admin, reply_to_user, send_reply
from handlers.users.settings import settings, change_notif

from states import states

from keyboards.inline.inline_tasks import menu_callback, tasks_callback, day_callback, reply_support_callback, \
    lang_callback

from handlers.users.settings import choose_language, change_lang
from handlers.users.start import close_menu_state, close_menu

from bot.handlers.users.today_plans import show_page
from bot.keyboards.inline.inline_tasks import pagination_call


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())

    dp.register_callback_query_handler(close_menu, text='close', State=None)
    dp.register_callback_query_handler(close_menu_state, text='close', state='*')
    dp.register_callback_query_handler(settings, text='back')
    dp.register_callback_query_handler(show_page,pagination_call.filter(key='items'))
    dp.register_message_handler(show_plans, text=['Планы на сегодня 📝', 'Плани на сьогодні 📝', 'Plans for today 📝'])

    dp.register_callback_query_handler(start_adding_task, menu_callback.filter(name='add_task'))
    dp.register_message_handler(add_task, state=states.Task.add_task)

    dp.register_callback_query_handler(choose_done, menu_callback.filter(name='done'))
    dp.register_callback_query_handler(mark_done, tasks_callback.filter(name='done_task')
                                       )

    dp.register_callback_query_handler(choose_del, menu_callback.filter(name='delete'))
    dp.register_callback_query_handler(delete_task, tasks_callback.filter(name='delete_task'))

    dp.register_callback_query_handler(choose_edit, menu_callback.filter(name='edit'))
    dp.register_callback_query_handler(start_editing, tasks_callback.filter(name='edit_task'))
    dp.register_message_handler(edit_task, state=states.Task.edit_task)

    dp.register_message_handler(choose_day, text=['Планы на неделю 📝', 'Плани на тиждень 📝', 'Plans for week 📝'])
    dp.register_callback_query_handler(show_week_plans, day_callback.filter(name='week_day'))

    dp.register_message_handler(support, text=['Обратная связь 📲', 'Тех.підтримка 📲', 'Support 📲'])
    dp.register_callback_query_handler(call_support, text='confirm')
    dp.register_message_handler(send_to_admin, state=states.Support.add_text, content_types=types.ContentType.ANY)
    dp.register_callback_query_handler(reply_to_user, reply_support_callback.filter(name='reply'))
    dp.register_message_handler(send_reply, state=states.Support.reply_msg)

    dp.register_message_handler(settings, text=['Настройки ⚙️', 'Налаштування ⚙️', 'Settings ⚙️'])
    dp.register_callback_query_handler(change_notif, text='change_notif')
    dp.register_callback_query_handler(change_lang, lang_callback.filter(name='lang'))
    dp.register_callback_query_handler(choose_language, text='change_language')
