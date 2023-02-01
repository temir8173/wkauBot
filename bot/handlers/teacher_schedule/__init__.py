from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ParseMode
from aioredis import Redis

from bot.keyboards.inline.ikb_select_options import generate_options, re_ask_options, day_of_week_options
from bot.messages import get_message
from bot.repositories.schedule_api_repository import get_option_value
from bot.repositories.schedule_repository import teacher_preferences, set_teacher_preferences
from bot.services import render_schedule_service
from bot.services.render_schedule_service import FOR_TEACHER


class FSMTeacherScheduleOptionsStates(StatesGroup):
    institute = State()
    high_school = State()
    teacher = State()
    week = State()
    day_of_week = State()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(ask_again_teacher, text=['ask_again_teacher'], state='*')
    dp.register_callback_query_handler(ask_institute_teacher, text=['teacherschedule'], state='*')
    dp.register_callback_query_handler(ask_high_school, state=FSMTeacherScheduleOptionsStates.institute)
    dp.register_callback_query_handler(ask_teacher, state=FSMTeacherScheduleOptionsStates.high_school)
    dp.register_callback_query_handler(ask_week, state=FSMTeacherScheduleOptionsStates.teacher)
    dp.register_callback_query_handler(ask_day_of_week, state=FSMTeacherScheduleOptionsStates.week)
    dp.register_callback_query_handler(render_schedule, state=FSMTeacherScheduleOptionsStates.day_of_week)


async def ask_institute_teacher(callback: CallbackQuery, state: FSMContext, redis: Redis, locale: Union[str, None]):
    preference = await teacher_preferences(callback.from_user.id, redis)
    await state.finish()
    if preference and preference[0].isnumeric() and preference[1].isnumeric() and preference[2].isnumeric():
        await FSMTeacherScheduleOptionsStates.teacher.set()
        async with state.proxy() as data:
            data['teacher_institute'] = preference[0]
            data['teacher_high_school'] = preference[1]
            data['teacher_teacher'] = preference[2]
        institute_name = await get_option_value(int(preference[0]), locale=locale)
        high_school_name = await get_option_value(int(preference[1]), int(preference[0]), 'teachers-school', locale)
        teacher_name = await get_option_value(int(preference[2]), int(preference[1]), 'teacher', locale)
        re_ask_buttons = await re_ask_options(preference[2], FOR_TEACHER, locale)
        await callback.message.reply(
            get_message(
                'teacher_preferences',
                locale,
                institute_name=institute_name,
                high_school_name=high_school_name,
                teacher_name=teacher_name,
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=re_ask_buttons
        )
    else:
        await ask_again_teacher(callback, locale)


async def ask_again_teacher(callback: CallbackQuery, locale: Union[str, None]):
    await FSMTeacherScheduleOptionsStates.institute.set()
    institutes = await generate_options(locale)
    await callback.message.reply(get_message('chose_institute', locale), reply_markup=institutes)


async def ask_high_school(callback: CallbackQuery, state: FSMContext, locale: Union[str, None]):
    parent_option_id = callback.data
    async with state.proxy() as data:
        data['teacher_institute'] = parent_option_id
    await FSMTeacherScheduleOptionsStates.next()

    schools = await generate_options(locale, parent_option_id, 'teachers-school')
    await callback.message.answer(get_message('chose_school', locale), reply_markup=schools)
    await callback.answer()


async def ask_teacher(callback: CallbackQuery, state: FSMContext, locale: Union[str, None]):
    parent_option_id = callback.data
    async with state.proxy() as data:
        data['teacher_high_school'] = parent_option_id
    await FSMTeacherScheduleOptionsStates.next()

    groups = await generate_options(locale, parent_option_id, 'teacher', True)
    await callback.message.reply(get_message('chose_teacher', locale), reply_markup=groups)
    await callback.answer()


async def ask_week(callback: CallbackQuery, state: FSMContext, locale: Union[str, None]):
    parent_option_id = callback.data
    async with state.proxy() as data:
        data['teacher_teacher'] = parent_option_id
    await FSMTeacherScheduleOptionsStates.next()

    weeks = await generate_options(locale, parent_option_id, 'teachers-week', True)
    await callback.message.reply(get_message('chose_week', locale), reply_markup=weeks)
    await callback.answer()


async def ask_day_of_week(callback: CallbackQuery, state: FSMContext, locale: Union[str, None]):
    parent_option_id = callback.data
    async with state.proxy() as data:
        data['teacher_week'] = parent_option_id
    await FSMTeacherScheduleOptionsStates.next()

    days_of_week = await day_of_week_options(locale)
    await callback.message.reply(get_message('chose_day', locale), reply_markup=days_of_week)
    await callback.answer()


async def render_schedule(callback: CallbackQuery, state: FSMContext, redis: Redis, locale: Union[str, None]):
    parent_option_id = callback.data
    async with state.proxy() as data:
        data['teacher_day_of_week'] = parent_option_id
        print(list(data.values()))
        await set_teacher_preferences(callback.from_user.id, list(data.values()), redis=redis)

    schedule_view = await render_schedule_service.view_for_teacher(*list(data.values()), locale=locale)
    days_of_week = await day_of_week_options(locale)
    await callback.message.reply(schedule_view, parse_mode=ParseMode.HTML, reply_markup=days_of_week)
    await callback.answer()
