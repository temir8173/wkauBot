SCHEDULE_MONDAY = 'monday'
SCHEDULE_TUESDAY = 'tuesday'
SCHEDULE_WEDNESDAY = 'wednesday'
SCHEDULE_THURSDAY = 'thursday'
SCHEDULE_FRIDAY = 'friday'
SCHEDULE_SATURDAY = 'saturday'


def convert_to_schedule_api_format(day: str) -> str:
    days_map = {
        SCHEDULE_MONDAY: "0",
        SCHEDULE_TUESDAY: "1",
        SCHEDULE_WEDNESDAY: "2",
        SCHEDULE_THURSDAY: "3",
        SCHEDULE_FRIDAY: "4",
        SCHEDULE_SATURDAY: "5",
    }

    return days_map[day]
