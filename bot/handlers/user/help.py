from typing import Union

from aiogram import types


async def bot_help(msg: types.Message, locale: Union[str, None]):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку'
    ]
    await msg.answer('\n'.join(text))
