from typing import Dict, Any

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aioredis import Redis
from sqlalchemy.orm import sessionmaker


class CustomMiddleware(BaseMiddleware):
    def __init__(self, session_maker: sessionmaker, redis: Redis):
        self.session_maker = session_maker
        self.redis = redis
        super().__init__()

    async def on_pre_process_message(self, message: Message, data: Dict[str, Any]):
        data["session_maker"] = self.session_maker
        data["redis"] = self.redis

    async def on_preprocess_update(self, update: types.Update, data: dict):
        print('Pre process update')

    async def on_process_update(self, update: types.Update, data: dict):
        print('Process update')

