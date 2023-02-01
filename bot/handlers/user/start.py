from typing import Union
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from bot.keyboards.inline import start_menu_markup
from bot.messages import get_message


async def bot_start(message: types.Message, state: FSMContext, locale: Union[str, None]):
    await state.finish()
    await message.answer(
        get_message(
            'start',
            locale,
            user=message.from_user.full_name if message.from_user.full_name else message.from_user.username
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=start_menu_markup.generate(locale)
    )
