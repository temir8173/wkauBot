from typing import Dict, Any

from bot.helpers.schedule_days_list import ScheduleDaysList
from bot.helpers.schedule_subject_types_list import translate
from bot.messages import get_message
from bot.repositories.schedule_api_repository import get_schedule, get_schedule_for_teacher

FOR_STUDENT = 0
FOR_TEACHER = 1
MAX_TIME_SLOTS = 9


async def view_for_student(institute: int, school: int, group: int, week: str, day_of_week: str, locale: str):
    schedule = await get_schedule(institute, school, group, week)

    return await render(schedule, day_of_week, FOR_STUDENT, locale)


async def view_for_teacher(institute: int, school: int, teacher: int, week: str, day_of_week: str, locale: str):
    schedule = await get_schedule_for_teacher(institute, school, teacher, week)

    return await render(schedule, day_of_week, FOR_TEACHER, locale)


async def render(schedule: Dict[str, Any], day_of_week: str, mode: int, locale: str):
    target_day = ScheduleDaysList(day_of_week, locale).convert_to_schedule_api_format()
    chosen_day_schedule = {
        time: days[target_day]
        for time, days in schedule['schedule'].items()
        if target_day in days
    }

    view = get_message('schedule_header', locale, mode=mode) + '\n\n'

    for time_index, time_value in schedule['times'].items():
        if int(time_index) > MAX_TIME_SLOTS:
            continue

        view += f'⏱ <b>{time_value}</b>\n'
        if str(time_index) not in chosen_day_schedule:
            view += f'      ➖ \n\n'
            continue

        view += _format_slot(chosen_day_schedule[str(time_index)], mode, locale)

    return view

def _format_slot(items: dict, mode: int, locale: str) -> str:
    subject_key = 'Predmet_kaz' if locale == 'kk' else 'Predmet'
    subjects, types, teachers, places = [], [], [], []
    for item in items.values():
        if item[subject_key] not in subjects:
            subjects.append(item[subject_key])
            types.append(translate(item["TipZ"], locale))
            if mode == FOR_TEACHER:
                places.append(item["Nomer"])
        teachers.append(item["FIO"] if mode == FOR_STUDENT else item["Gruppa"])
        if mode == FOR_STUDENT:
            places.append(item["Nomer"])

    return (
        f'✔️ <b>{" / ".join(subjects)}</b>\n'
        f'✔️ <i>{" / ".join(types)}</i>\n'
        f'✔️ {" / ".join(teachers)}\n'
        f'✔️ {" / ".join(places)}\n\n'
    )
