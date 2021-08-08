from aiogram import types

from keyboards.inline.inline_tasks import week_day_kb, change_tasks_kb
from utils.db_api import db_func as db
from bot.reqi import _, _l


async def choose_day(message: types.Message):
    await message.answer(_('Выберите день недели'), reply_markup=await week_day_kb(message.from_user.id))


async def show_week_plans(call: types.CallbackQuery, callback_data: dict):
    day = int(callback_data.get('day'))
    tasks = await db.get_tasks(call.from_user.id, day)
    t = []
    t_done = []
    for task_id, task, done in tasks:
        if done:
            t_done.append(f'✅ {task}')
        else:
            t.append(f'🚫 {task}')

    if len(t_done) != 0:
        done_tasks = _l("\n\n<b>Выполненные задачи:</b>\n") + "\n".join(t_done)
    else:
        done_tasks = ''
    week = ([_('Понедельник'), _('Вторник'), _('Среду'), _('Четверг'), _('Пятницу'), _('Суботу'), _('Воскресенье')])
    await call.message.answer(_("<b>Ваши планы на {day}:</b>\n").format(day=week[day]) + "\n".join(t) + done_tasks,
                              reply_markup=await change_tasks_kb(day))
