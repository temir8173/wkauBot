from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ParseMode
from aioredis import Redis

from bot.keyboards.inline.ikb_select_options import generate_options, re_ask_options, day_of_week_options
from bot.messages import get_message
from bot.repositories.schedule_api_repository import get_option_value
from bot.repositories.schedule_repository import student_preferences, set_student_preferences
from bot.services import render_schedule_service
from bot.services.render_schedule_service import FOR_STUDENT


class FSMStudentScheduleOptions(StatesGroup):
    institute = State()
    high_school = State()
    group = State()
    week = State()
    day_of_week = State()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(ask_again, text=['ask_again'], state='*')
    dp.register_callback_query_handler(ask_institute, text=['studentschedule'], state='*')
    dp.register_callback_query_handler(ask_high_school, state=FSMStudentScheduleOptions.institute)
    dp.register_callback_query_handler(ask_group, state=FSMStudentScheduleOptions.high_school)
    dp.register_callback_query_handler(ask_week, state=FSMStudentScheduleOptions.group)
    dp.register_callback_query_handler(ask_day_of_week, state=FSMStudentScheduleOptions.week)
    dp.register_callback_query_handler(render_schedule, state=FSMStudentScheduleOptions.day_of_week)


async def ask_institute(callback: CallbackQuery, state: FSMContext, redis: Redis, locale: Union[str, None]):
    preference = await student_preferences(callback.from_user.id, redis)
    await state.finish()
    if preference and preference[0].isnumeric() and preference[1].isnumeric() and preference[2].isnumeric():
        await FSMStudentScheduleOptions.group.set()
        async with state.proxy() as data:
            data['student_institute'] = preference[0]
            data['student_high_school'] = preference[1]
            data['student_group'] = preference[2]
        institute_name = await get_option_value(int(preference[0]), locale=locale)
        high_school_name = await get_option_value(int(preference[1]), int(preference[0]), 'school', locale)
        group_name = await get_option_value(int(preference[2]), int(preference[1]), 'group', locale)
        re_ask_buttons = await re_ask_options(preference[2], FOR_STUDENT, locale)
        await callback.message.reply(
            get_message(
                'student_preferences',
                locale,
                institute_name=institute_name,
                high_school_name=high_school_name,
                group_name=group_name,
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=re_ask_buttons
        )
    else:
        await ask_again(callback, locale)


async def ask_again(callback: CallbackQuery, locale: Union[str, None]):
    await FSMStudentScheduleOptions.institute.set()
    institutes = await generate_options(locale)
    await callback.message.reply(get_message('chose_institute', locale), reply_markup=institutes)


async def ask_high_school(callback: CallbackQuery, state: FSMContext, locale: Union[str, None]):
    parent_option_id = callback.data
    async with state.proxy() as data:
        data['student_institute'] = parent_option_id
    await FSMStudentScheduleOptions.next()

    schools = await generate_options(locale, parent_option_id, 'school')
    await callback.message.answer(get_message('chose_school', locale), reply_markup=schools)
    await callback.answer()


async def ask_group(callback: CallbackQuery, state: FSMContext, locale: Union[str, None]):
    parent_option_id = callback.data
    async with state.proxy() as data:
        data['student_high_school'] = parent_option_id
    await FSMStudentScheduleOptions.next()

    groups = await generate_options(locale, parent_option_id, 'group', True)
    await callback.message.reply(get_message('chose_group', locale), reply_markup=groups)
    await callback.answer()


async def ask_week(callback: CallbackQuery, state: FSMContext, locale: Union[str, None]):
    parent_option_id = callback.data
    async with state.proxy() as data:
        data['student_group'] = parent_option_id
    await FSMStudentScheduleOptions.next()

    weeks = await generate_options(locale, parent_option_id, 'week', True)
    await callback.message.reply(get_message('chose_week', locale), reply_markup=weeks)
    await callback.answer()


async def ask_day_of_week(callback: CallbackQuery, state: FSMContext, locale: Union[str, None]):
    parent_option_id = callback.data
    async with state.proxy() as data:
        data['student_week'] = parent_option_id
    await FSMStudentScheduleOptions.next()

    days_of_week = await day_of_week_options(locale)
    await callback.message.reply(get_message('chose_day', locale), reply_markup=days_of_week)
    await callback.answer()


async def render_schedule(callback: CallbackQuery, state: FSMContext, redis: Redis, locale: Union[str, None]):
    parent_option_id = callback.data
    async with state.proxy() as data:
        data['student_day_of_week'] = parent_option_id
        await set_student_preferences(callback.from_user.id, list(data.values()), redis=redis)

    schedule_view = await render_schedule_service.view_for_student(*list(data.values()), locale=locale)
    days_of_week = await day_of_week_options(locale)
    await callback.message.reply(schedule_view, parse_mode=ParseMode.HTML, reply_markup=days_of_week)
    await callback.answer()
