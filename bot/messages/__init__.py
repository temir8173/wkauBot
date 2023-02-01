import bot.messages.main_messages
from bot.messages import schedule_messages, start_menu_options, settings_messages


def get_message(key: str, locale: str, **kwargs) -> str:
    if key not in MESSAGES or locale not in MESSAGES[key]:
        message = '-'
    else:
        message = MESSAGES[key][locale]
    return message.format(**kwargs)


MESSAGES = {
    # основные текста
    'start': main_messages.start,

    # текста меню настроек
    'settings_main': settings_messages.settings_main,
    'change_lang': settings_messages.change_lang,
    'lang_changed': settings_messages.lang_changed,
    'choose_lang': settings_messages.choose_lang,

    # стартовое меню
    'menu_student_schedule': start_menu_options.menu_student_schedule,
    'menu_teacher_schedule': start_menu_options.menu_teacher_schedule,

    # текста расписания
    'teacher_preferences': schedule_messages.teacher_preferences,
    'student_preferences': schedule_messages.student_preferences,
    'chose_institute': schedule_messages.chose_institute,
    'chose_school': schedule_messages.chose_school,
    'chose_teacher': schedule_messages.chose_teacher,
    'chose_group': schedule_messages.chose_group,
    'chose_week': schedule_messages.chose_week,
    'chose_day': schedule_messages.chose_day,
    'schedule_header': schedule_messages.schedule_header,
    're_enter_option': schedule_messages.re_enter_option,
    'go_further_option': schedule_messages.go_further_option,
}
