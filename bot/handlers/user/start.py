from aiogram import types

from bot.keyboards.inline.ikb_select_options import ikbSelectOptions


async def bot_start(msg: types.Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!', reply_markup=ikbSelectOptions)
