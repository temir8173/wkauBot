from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_menu_keyboard = InlineKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
ikb_student_schedule = InlineKeyboardButton(text='Студенттерге арналған сабақ кестесі', callback_data='studentschedule')
ikb_teacher_schedule = InlineKeyboardButton(text='Оқытушыларға арналған сабақ кестесі', callback_data='teacherschedule')

start_menu_keyboard.add(ikb_student_schedule).add(ikb_teacher_schedule)
