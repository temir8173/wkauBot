#  Copyright (c) 2022.

from typing import Dict, Any

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aioredis import Redis
from sqlalchemy.orm import sessionmaker

from bot.repositories.user_repository import is_user_exists, create_user


class RegisterCheck(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: Dict[str, Any]):
        pass

    async def on_process_message(
            self,
            message: types.Message,
            data: Dict[str, Any],
    ) -> Any:
        print('register')
        print(message)
        session_maker: sessionmaker = data['session_maker']
        redis: Redis = data['redis']
        user = message.from_user
        if not await is_user_exists(user_id=user.id, session_maker=session_maker, redis=redis):
            await create_user(user_id=user.id,
                              username=user.username,
                              session_maker=session_maker,
                              redis=redis,
                              locale=user.language_code
                              )
            await message.bot.send_message(message.chat.id, 'Ты успешно зарегистрирован(а)!')

        # return await handler(message, data)
