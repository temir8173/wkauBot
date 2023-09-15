from typing import Dict, Any

from bot.helpers.schedule_days_list import ScheduleDaysList
from bot.helpers.schedule_subject_types_list import translate
from bot.messages import get_message
from bot.repositories.schedule_api_repository import get_schedule, get_schedule_for_teacher

FOR_STUDENT = 0
FOR_TEACHER = 1


async def view_for_student(institute: int, school: int, group: int, week: str, day_of_week: str, locale: str):
    schedule = await get_schedule(institute, school, group, week)

    return await render(schedule, day_of_week, FOR_STUDENT, locale)


async def view_for_teacher(institute: int, school: int, teacher: int, week: str, day_of_week: str, locale: str):
    schedule = await get_schedule_for_teacher(institute, school, teacher, week)

    return await render(schedule, day_of_week, FOR_TEACHER, locale)


async def render(schedule: Dict[str, Any], day_of_week: str, mode: int, locale: str):
    chosen_day_schedule = {}
    for time in schedule['schedule']:
        for day in schedule['schedule'][time]:
            day_instance = ScheduleDaysList(day_of_week, locale)
            if day_instance.convert_to_schedule_api_format() == day:
                chosen_day_schedule[time] = schedule['schedule'][time][day]

    chosen_day_schedule = dict(sorted(chosen_day_schedule.items()))

    view = get_message('schedule_header', locale, mode=mode) + '\n\n'

    for time_index, time_value in schedule['times'].items():
        if int(time_index) > 9:
            continue

        view += f'⏱ <b>{time_value}</b>\n'
        if str(time_index) not in chosen_day_schedule:
            view += f'      ➖ \n\n'
            continue

        subject = ''
        subject_type = ''
        teacher_or_group = ''
        place = ''
        subject_key = 'Predmet_kaz' if locale == 'kk' else 'Predmet'
        for schedule_item in chosen_day_schedule[str(time_index)].values():
            if subject.find(schedule_item[subject_key]) == -1:
                subject += f'{schedule_item[subject_key]} / '
                subject_type += f'{translate(schedule_item["TipZ"], locale)} / '
            if mode == FOR_STUDENT:
                teacher_or_group += f'{schedule_item["FIO"]} / '
            else:
                teacher_or_group += f'{schedule_item["Gruppa"]} / '
            place += f'{schedule_item["Nomer"]} / '

        view += f'✔ ️<b>{subject[:-3]}</b>\n' \
                f'✔️ <i>{subject_type[:-3]}</i>\n' \
                f'✔ ️{teacher_or_group[:-3]}\n' \
                f'✔️ {place[:-3]}\n\n'

    return view
