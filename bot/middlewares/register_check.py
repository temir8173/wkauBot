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
        """ Сама функция для обработки вызова """
        print(message)
        print(data)
        print(self.session_maker)
        # session_maker = data['session_maker']
        # redis = data['redis']
        # user = event.from_user
        # if not await is_user_exists(user_id=event.from_user.id, session_maker=session_maker, redis=redis):
        #     await create_user(user_id=event.from_user.id,
        #                       username=event.from_user.username, session_maker=session_maker, locale=user.language_code)
        #     await data['bot'].send_message(event.from_user.id, 'Ты успешно зарегистрирован(а)!')
        #
        # return await handler(event, data)
