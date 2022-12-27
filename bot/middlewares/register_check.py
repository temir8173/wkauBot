#  Copyright (c) 2022.

from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aioredis import Redis
from sqlalchemy.orm import sessionmaker

from bot.repositories.user_repository import is_user_exists, create_user


class RegisterCheck(BaseMiddleware):
    def __init__(self, session_maker: sessionmaker, redis: Redis):
        self.session_maker = session_maker
        self.redis = redis
        super().__init__()

    async def on_process_message(
            self,
            message: types.Message,
            data: Dict[str, Any],
    ) -> Any:
        print('register')
        print(message)
        user = message.from_user
        if not await is_user_exists(user_id=user.id, session_maker=self.session_maker, redis=self.redis):
            await create_user(user_id=user.id,
                              username=user.username, session_maker=self.session_maker, locale=user.language_code)
            await message.bot.send_message(message.chat.id, 'Ты успешно зарегистрирован(а)!')

        # return await handler(message, data)
