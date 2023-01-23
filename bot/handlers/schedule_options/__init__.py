from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot.models import User

from bot.repositories.schedule_repository import student_preferences
from aioredis import Redis
from sqlalchemy.orm import sessionmaker


class FSMStudentScheduleOptions(StatesGroup):
    institute = State()
    high_school = State()
    group = State()
    week = State()


def setup(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['studentschedule'], state='*')
    dp.register_message_handler(ask_institute, state=FSMStudentScheduleOptions.institute)
    dp.register_message_handler(ask_high_school, state=FSMStudentScheduleOptions.high_school)
    dp.register_message_handler(ask_group, state=FSMStudentScheduleOptions.group)
    dp.register_message_handler(ask_week, state=FSMStudentScheduleOptions.week)


async def cm_start(message: types.Message, state: FSMContext, session_maker: sessionmaker, redis: Redis):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).where(User.user_id == 406772693))
            user: User = sql_res.scalar_one_or_none()
            print('user')
            print(user.username)
    options = await student_preferences(message.from_user.id, session, redis)
    print(options)
    await FSMStudentScheduleOptions.institute.set()
    async with state.proxy() as data:
        await message.reply(str(data)) 
    await message.reply('Институт таңдаңыз')


async def ask_institute(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['student_institute'] = message.text
    await FSMStudentScheduleOptions.next()
    async with state.proxy() as data:
        await message.reply(str(data))
    await message.reply('Жоғары мектеп таңдаңыз')


async def ask_high_school(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['student_high_school'] = message.text
    await FSMStudentScheduleOptions.next()
    async with state.proxy() as data:
        await message.reply(str(data))
    await message.reply('Топ таңдаңыз')


async def ask_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['student_group'] = message.text
    await FSMStudentScheduleOptions.next()
    async with state.proxy() as data:
        await message.reply(str(data))
    await message.reply('Апта таңдаңыз')


async def ask_week(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['student_week'] = message.text
    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()
