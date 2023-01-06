from aiogram import types

from bot.keyboards.inline.ikb_test import ikbTest


async def bot_start(msg: types.Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!', reply_markup=ikbTest)
