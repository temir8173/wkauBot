from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.messages import get_message


def generate(locale: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    ikb_change_lang = InlineKeyboardButton(
        text=get_message('change_lang', locale),
        callback_data='change-lang'
    )

    return kb.add(ikb_change_lang)


def languages():
    kb = InlineKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    ikb_change_lang_kk = InlineKeyboardButton(text='🇰🇿 Қазақ', callback_data='change-lang-kk')
    ikb_change_lang_ru = InlineKeyboardButton(text='🇷🇺 Русский', callback_data='change-lang-ru')

    return kb.add(ikb_change_lang_kk).add(ikb_change_lang_ru)
