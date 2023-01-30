import bot.messages.main_messages

MESSAGES = {
    'start': {
        'kk': main_messages.start_message,
        'ru': main_messages.start_message_ru,
    },
    # 'help': help_message,
    # 'invalid_key': invalid_key_message,
    # 'state_change': state_change_success_message,
    # 'state_reset': state_reset_message,
    # 'current_state': current_state_message,
}


def get_message(key: str, locale: str, **kwargs) -> str:
    if key not in MESSAGES or locale not in MESSAGES[key]:
        message = 'no message'
    else:
        message = MESSAGES[key][locale]
    return message.format(**kwargs)
