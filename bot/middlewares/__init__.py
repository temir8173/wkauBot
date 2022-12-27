from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .register_check import RegisterCheck
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LoggingMiddleware())
