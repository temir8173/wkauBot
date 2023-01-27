from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb = KeyboardButton(text='Бас мәзір', callback_data='start')
main_menu_markup.add(kb)
