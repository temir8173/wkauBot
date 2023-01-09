import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aioredis import Redis
from aiohttp import web

from bot.middlewares.register_check import RegisterCheck
from bot.middlewares.custom_middleware import CustomMiddleware
from bot.config import TOKEN, REDIS_PASSWORD, REDIS_HOST, SQLALCHEMY_ASYNC_DB_URI
from bot.db import create_async_engine, get_session_maker


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)

async_engine = create_async_engine(SQLALCHEMY_ASYNC_DB_URI)
session_maker = get_session_maker(async_engine)

redis = Redis(
        host=REDIS_HOST,
        password=REDIS_PASSWORD
    )

# PROXY_URL = "http://37.53.103.4:3128"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=RedisStorage2(host=REDIS_HOST, password=REDIS_PASSWORD))

dp.middleware.setup(LoggingMiddleware())
# dp.middleware.setup(CustomMiddleware(session_maker=session_maker, redis=redis))
dp.middleware.setup(RegisterCheck(session_maker=session_maker, redis=redis))


# noinspection PyUnusedLocal
async def on_startup(app: web.Application):
    # import middlewares
    # import filters
    # middlewares.setup(dp)
    # filters.setup(dp)
    print('asasd')
    import bot.handlers as handlers

    print('asasd')
    handlers.schedule_options.setup(dp)
    handlers.errors.setup(dp)
    handlers.user.setup(dp)


async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    print('ok')
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)



# import redis
#
# r = redis.Redis(host='redis', port=6379, db=0)
# r.set('foo', 'bar')
# print(r.get('foo'))