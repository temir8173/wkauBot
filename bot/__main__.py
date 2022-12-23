import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aioredis import Redis
from sqlalchemy.engine import URL  # type: ignore

from bot.middlewares.register_check import RegisterCheck
from bot.middlewares.custom_middleware import CustomMiddleware
from bot.config import TOKEN, REDIS_PASSWORD, REDIS_HOST, SQLALCHEMY_ASYNC_DB_URI
from bot.messages import MESSAGES
from bot.utils import TestStates
from bot.db import create_async_engine, get_session_maker


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)

async_engine = create_async_engine(SQLALCHEMY_ASYNC_DB_URI)
session_maker = get_session_maker(async_engine)

redis = Redis(
        host=REDIS_HOST,
        password=REDIS_PASSWORD,
        username=None,
    )

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=RedisStorage2(host=REDIS_HOST, password=REDIS_PASSWORD))
# dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(CustomMiddleware())
dp.middleware.setup(RegisterCheck(session_maker=session_maker, redis=redis))


@dp.message_handler(state='*', commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(MESSAGES['start'])


@dp.message_handler(state='*', commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['help'])


@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['state_reset'])

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply(MESSAGES['invalid_key'].format(key=argument))

    await state.set_state(TestStates.all()[int(argument)])
    await message.reply(MESSAGES['state_change'], reply=False)

@staticmethod
@dp.message_handler(state=TestStates.TEST_STATE_1)
async def first_test_state_case_met(message: types.Message):
    await message.reply('Первый!', reply=False)


@dp.message_handler(state=TestStates.TEST_STATE_2[0])
async def second_test_state_case_met(message: types.Message):
    await message.reply('Второй!', reply=False)


@dp.message_handler(state=TestStates.TEST_STATE_3 | TestStates.TEST_STATE_4)
async def third_or_fourth_test_state_case_met(message: types.Message):
    await message.reply('Третий или четвертый!', reply=False)


@dp.message_handler(state=TestStates.all())
async def some_test_state_case_met(message: types.Message):
    text = MESSAGES['current_state'].format(
        current_state=await dp.current_state(user=message.from_user.id).get_state(),
        states=TestStates.all()
    )

    # with dp.current_state(user=message.from_user.id) as state:
    #     text = MESSAGES['current_state'].format(
    #         current_state=5, #await state.get_state(),
    #         states=TestStates.all()
    #     )
    await message.reply(text, reply=False)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    print('ok')
    executor.start_polling(dp, on_shutdown=shutdown)



# import redis
#
# r = redis.Redis(host='redis', port=6379, db=0)
# r.set('foo', 'bar')
# print(r.get('foo'))