SUBJECT_TYPE_LABORATORY = 'Лаб.'
SUBJECT_TYPE_LECTURE = 'Лек.'
SUBJECT_TYPE_PRACTICAL = 'Пр.'
SUBJECT_TYPE_PBS = 'ПБС'
SUBJECT_TYPE_OTHER = 'other'


def get_kk_translation(subject_type: str) -> str:
    translations = {
        SUBJECT_TYPE_LABORATORY: "Зертханалық",
        SUBJECT_TYPE_LECTURE: "Дәріс",
        SUBJECT_TYPE_PRACTICAL: "Тәжірибелік",
        SUBJECT_TYPE_PBS: "ПБС",
        SUBJECT_TYPE_OTHER: "Басқа",
    }

    return translations[subject_type]


def get_ru_translation(subject_type: str) -> str:
    translations = {
        SUBJECT_TYPE_LABORATORY: "Лабораторное",
        SUBJECT_TYPE_LECTURE: "Лекция",
        SUBJECT_TYPE_PRACTICAL: "Практическое",
        SUBJECT_TYPE_PBS: "ПОЗ",
        SUBJECT_TYPE_OTHER: "Другие",
    }

    return translations[subject_type]


def translate(subject_type: str) -> str:
    # TODO: сделать нормально
    locale = 'kk'
    if locale == 'kk':
        return get_kk_translation(subject_type)
    elif locale == 'ru':
        return get_ru_translation(subject_type)
