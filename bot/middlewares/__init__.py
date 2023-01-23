from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aioredis import Redis
from sqlalchemy.orm import sessionmaker

from .custom_middleware import CustomMiddleware
from .register_check import RegisterCheck
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher, session_maker: sessionmaker, redis: Redis):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(CustomMiddleware(session_maker=session_maker, redis=redis))
    dp.middleware.setup(RegisterCheck())
