from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from gino import Gino
from sqlalchemy import Column

from data import config

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer(), unique=True)
    username = db.Column(db.Unicode())
    fullname = db.Column(db.Unicode())
    notif = db.Column(db.Boolean(), default=True)
    language = db.Column(db.String(2), default='ru')
    created_at = Column(db.DateTime(True), server_default=db.func.now())
    updated_at = Column(db.DateTime(True),
                        default=db.func.now(),
                        onupdate=db.func.now(),
                        server_default=db.func.now(), )


class Tasks(db.Model):
    __tablename__ = 'tasks'

    user_id = db.Column(db.Integer())
    task_id = db.Column(db.BigInteger(), primary_key=True)
    task = db.Column(db.String())
    day = db.Column(db.Integer())
    done = db.Column(db.Boolean(), default=False)


async def on_startup(dispatcher: Dispatcher):
    await db.set_bind(config.POSTGRES_URI)


def setup(executor: Executor):
    executor.on_startup(on_startup)