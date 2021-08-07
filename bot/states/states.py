from aiogram.dispatcher.filters.state import StatesGroup, State


class Task(StatesGroup):
    add_task = State()
    edit_task = State()


class Support(StatesGroup):
    add_text = State()
    reply_msg = State()
