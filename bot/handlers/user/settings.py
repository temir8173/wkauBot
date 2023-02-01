from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from bot.keyboards.inline import settings_keyboard
from bot.messages import get_message


async def bot_settings(message: types.Message, state: FSMContext, locale: Union[str, None]):
    await state.finish()
    await message.answer(
        get_message(
            'settings_main',
            locale
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=settings_keyboard.generate(locale)
    )
