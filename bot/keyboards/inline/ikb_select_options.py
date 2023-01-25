from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.repositories.schedule_api_repository import get_options

ikbSelectOptions = InlineKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)


async def generate_options(
    parent_option_id: int = None,
    target: str = 'institute',
    row_format: bool = False
) -> InlineKeyboardMarkup:
    ikbSelectOptions.inline_keyboard = []
    options = await get_options(parent_option_id, target)
    for option in options:
        ikb = InlineKeyboardButton(text=option['value'], callback_data=option['id'])
        if row_format:
            ikbSelectOptions.insert(ikb)
        else:
            ikbSelectOptions.add(ikb)

    return ikbSelectOptions


async def re_ask_options(week_id: str) -> InlineKeyboardMarkup:
    ikbSelectOptions.inline_keyboard = []
    ikb_re_answer = InlineKeyboardButton(text='Жоқ, қайтадан енгізу', callback_data='ask_again')
    ikb_go_further = InlineKeyboardButton(text='Иә, апта таңдау', callback_data=week_id)

    return ikbSelectOptions.add(ikb_re_answer).add(ikb_go_further)


async def day_of_week_options() -> InlineKeyboardMarkup:
    ikbSelectOptions.inline_keyboard = []
    ikb_monday = InlineKeyboardButton(text='Дс', callback_data='monday')
    ikb_tuesday = InlineKeyboardButton(text='Сс', callback_data='tuesday')
    ikb_wednesday = InlineKeyboardButton(text='Ср', callback_data='wednesday')
    ikb_thursday = InlineKeyboardButton(text='Бс', callback_data='thursday')
    ikb_friday = InlineKeyboardButton(text='Жм', callback_data='friday')
    ikb_saturday = InlineKeyboardButton(text='Сн', callback_data='saturday')

    return ikbSelectOptions.add(ikb_monday, ikb_tuesday, ikb_wednesday, ikb_thursday, ikb_friday, ikb_saturday)
