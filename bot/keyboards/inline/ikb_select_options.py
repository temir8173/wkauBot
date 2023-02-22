from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.helpers.schedule_days_list import ScheduleDaysList
from bot.messages import get_message
from bot.repositories.schedule_api_repository import get_options
from bot.services.render_schedule_service import FOR_STUDENT

ikbSelectOptions = InlineKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)


async def generate_options(
    locale: str,
    parent_option_id: int = None,
    target: str = 'institute',
    row_format: bool = False
) -> InlineKeyboardMarkup:
    ikbSelectOptions.inline_keyboard = []
    options = await get_options(parent_option_id, target, locale)
    for option in options:
        ikb = InlineKeyboardButton(text=option['value'], callback_data=option['id'])
        if row_format:
            ikbSelectOptions.insert(ikb)
        else:
            ikbSelectOptions.add(ikb)

    return ikbSelectOptions


async def re_ask_options(week_id: str, mode: str, locale: str) -> InlineKeyboardMarkup:
    ikbSelectOptions.inline_keyboard = []
    re_ask_callback_data = 'ask_again' if mode == FOR_STUDENT else 'ask_again_teacher'
    ikb_re_answer = InlineKeyboardButton(
        text=get_message('re_enter_option', locale),
        callback_data=re_ask_callback_data
    )
    ikb_go_further = InlineKeyboardButton(text=get_message('go_further_option', locale), callback_data=week_id)

    return ikbSelectOptions.add(ikb_re_answer).add(ikb_go_further)


async def day_of_week_options(locale: str) -> InlineKeyboardMarkup:
    ikbSelectOptions.inline_keyboard = []
    monday = ScheduleDaysList(ScheduleDaysList.SCHEDULE_MONDAY, locale)
    tuesday = ScheduleDaysList(ScheduleDaysList.SCHEDULE_TUESDAY, locale)
    wednesday = ScheduleDaysList(ScheduleDaysList.SCHEDULE_WEDNESDAY, locale)
    thursday = ScheduleDaysList(ScheduleDaysList.SCHEDULE_THURSDAY, locale)
    friday = ScheduleDaysList(ScheduleDaysList.SCHEDULE_FRIDAY, locale)
    saturday = ScheduleDaysList(ScheduleDaysList.SCHEDULE_SATURDAY, locale)

    ikb_monday = InlineKeyboardButton(text=monday.translate(), callback_data=monday.day)
    ikb_tuesday = InlineKeyboardButton(text=tuesday.translate(), callback_data=tuesday.day)
    ikb_wednesday = InlineKeyboardButton(text=wednesday.translate(), callback_data=wednesday.day)
    ikb_thursday = InlineKeyboardButton(text=thursday.translate(), callback_data=thursday.day)
    ikb_friday = InlineKeyboardButton(text=friday.translate(), callback_data=friday.day)
    ikb_saturday = InlineKeyboardButton(text=saturday.translate(), callback_data=saturday.day())

    return ikbSelectOptions.add(ikb_monday, ikb_tuesday, ikb_wednesday, ikb_thursday, ikb_friday, ikb_saturday)
