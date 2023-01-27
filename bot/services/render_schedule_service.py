from typing import Dict, Any

from bot.helpers.schedule_days_list import convert_to_schedule_api_format
from bot.helpers.schedule_subject_types_list import translate
from bot.repositories.schedule_api_repository import get_schedule, get_schedule_for_teacher

FOR_STUDENT = 0
FOR_TEACHER = 1


async def view_for_student(institute: int, school: int, group: int, week: str, day_of_week: str):
    schedule = await get_schedule(institute, school, group, week)

    return await render(schedule, day_of_week, FOR_STUDENT)


async def view_for_teacher(institute: int, school: int, teacher: int, week: str, day_of_week: str):
    schedule = await get_schedule_for_teacher(institute, school, teacher, week)

    return await render(schedule, day_of_week, FOR_TEACHER)


async def render(schedule: Dict[str, Any], day_of_week: str, mode: int):
    chosen_day_schedule = {}
    for time in schedule['schedule']:
        for day in schedule['schedule'][time]:
            if convert_to_schedule_api_format(day_of_week) == day:
                chosen_day_schedule[time] = schedule['schedule'][time][day]

    chosen_day_schedule = dict(sorted(chosen_day_schedule.items()))

    view = f'📋 Сабақ кестесі \n\n'

    for time_index, time_value in enumerate(schedule['times']):
        if time_index > 9:
            continue

        view += f'⏱ <b>{time_value}</b>\n'
        if str(time_index) not in chosen_day_schedule:
            view += f'      ➖ \n\n'
            continue

        subject = ''
        subject_type = ''
        teacher_or_group = ''
        place = ''
        for index, schedule_item in enumerate(chosen_day_schedule[str(time_index)]):
            if subject.find(schedule_item['Predmet_kaz']) == -1:
                subject += f'{schedule_item["Predmet_kaz"]} / '
                subject_type += f'{translate(schedule_item["TipZ"])} / '
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
