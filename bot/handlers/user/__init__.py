from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp, CommandSettings

from .change_lang import change_lang
from .help import bot_help
from .settings import bot_settings
from .start import bot_start


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart(), state='*')
    dp.register_message_handler(bot_help, CommandHelp())
    dp.register_message_handler(bot_settings, CommandSettings(), state='*')
    dp.register_callback_query_handler(change_lang, text=['change-lang', 'change-lang-kk', 'change-lang-ru'], state='*')
