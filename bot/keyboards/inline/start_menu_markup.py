from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.messages import get_message


def generate(locale: str) -> InlineKeyboardMarkup:
    start_menu_keyboard = InlineKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    ikb_student_schedule = InlineKeyboardButton(
        text=get_message('menu_student_schedule', locale),
        callback_data='studentschedule'
    )
    ikb_teacher_schedule = InlineKeyboardButton(
        text=get_message('menu_teacher_schedule', locale),
        callback_data='teacherschedule'
    )

    return start_menu_keyboard.add(ikb_student_schedule).add(ikb_teacher_schedule)
