from enum import Enum
from typing import List

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api.database import User, Tasks


async def add_user(user_id: int, username: str, full_name: str):
    try:
        await User.create(user_id=user_id, username=username,
                          fullname=full_name)
    except UniqueViolationError:
        await User.update.values(username=username, fullname=full_name).where(
            'user_id' == user_id).gino.status()


async def add_task(user_id: int, task: str, day: int):
    await Tasks.create(user_id=user_id, task=task, day=day)


async def get_tasks(user_id: int, day: int) -> List[tuple]:
    return await Tasks.select('task_id', 'task', 'done').where(
        and_(Tasks.user_id == user_id, Tasks.day == day)).gino.all()


async def mark_done(task_id: int):
    await Tasks.update.values(done=True).where(Tasks.task_id == task_id).gino.status()


async def delete_task(task_id: int):
    await Tasks.delete.where(Tasks.task_id == task_id).gino.status()


async def get_task(task_id: int) -> str:
    return await Tasks.select('task').where(Tasks.task_id == task_id).gino.scalar()


async def edit_task(task_id: int, task: str):
    await Tasks.update.values(task=task).where(Tasks.task_id == task_id).gino.status()


async def get_users() -> [tuple]:
    return await User.select('user_id').gino.all()


async def get_users_notif() -> [tuple]:
    return await User.select('user_id').where(User.notif is True).gino.all()


async def get_notif(user_id: int) -> bool:
    return await User.select('notif').where(User.user_id == user_id).gino.scalar()


async def change_notif(user_id: int):
    if await get_notif(user_id):
        notif = False
    else:
        notif = True
    await User.update.values(notif=notif).where(User.user_id == user_id).gino.status()
