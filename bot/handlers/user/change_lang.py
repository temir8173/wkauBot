from typing import Union
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from sqlalchemy.orm import sessionmaker

from bot.keyboards.inline import settings_keyboard
from bot.messages import get_message
from bot.repositories.user_repository import update_locale


async def change_lang(
        callback: types.CallbackQuery,
        state: FSMContext,
        locale: Union[str, None],
        session_maker: sessionmaker
):
    if callback.data == 'change-lang':
        await state.finish()
        await callback.message.answer(
            get_message('choose_lang', locale),
            parse_mode=ParseMode.HTML,
            reply_markup=settings_keyboard.languages()
        )
        await callback.answer()
    elif callback.data == 'change-lang-kk' or callback.data == 'change-lang-ru':
        new_locale = callback.data[-2:]
        print('new_locale')
        print(new_locale)
        await update_locale(callback.from_user.id, new_locale, session_maker)
        await callback.message.answer(get_message('lang_changed', new_locale))
        # await bot_start(callback.message, state, new_locale)
        await callback.answer()
