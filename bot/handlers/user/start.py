from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.keyboards.inline.start_menu_markup import start_menu_keyboard


async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        f'Сәлем, {message.from_user.full_name}! \n'
        f'Жәңгір хан университетінің телеграм-ботына қош келдіңіз',
        reply_markup=start_menu_keyboard
    )
