class ScheduleDaysList:
    SCHEDULE_MONDAY = 'monday'
    SCHEDULE_TUESDAY = 'tuesday'
    SCHEDULE_WEDNESDAY = 'wednesday'
    SCHEDULE_THURSDAY = 'thursday'
    SCHEDULE_FRIDAY = 'friday'
    SCHEDULE_SATURDAY = 'saturday'

    def __init__(self, day, locale):
        self.day = day
        self.locale = locale

    def convert_to_schedule_api_format(self) -> str:
        days_map = {
            self.SCHEDULE_MONDAY: "0",
            self.SCHEDULE_TUESDAY: "1",
            self.SCHEDULE_WEDNESDAY: "2",
            self.SCHEDULE_THURSDAY: "3",
            self.SCHEDULE_FRIDAY: "4",
            self.SCHEDULE_SATURDAY: "5",
        }

        return days_map[self.day]

    def translate(self) -> str:
        translation = {
            'kk': {
                self.SCHEDULE_MONDAY: "Дс",
                self.SCHEDULE_TUESDAY: "Сс",
                self.SCHEDULE_WEDNESDAY: "Ср",
                self.SCHEDULE_THURSDAY: "Бс",
                self.SCHEDULE_FRIDAY: "Жм",
                self.SCHEDULE_SATURDAY: "Сн",
            },
            'ru': {
                self.SCHEDULE_MONDAY: "Пн",
                self.SCHEDULE_TUESDAY: "Вт",
                self.SCHEDULE_WEDNESDAY: "Ср",
                self.SCHEDULE_THURSDAY: "Чт",
                self.SCHEDULE_FRIDAY: "Пт",
                self.SCHEDULE_SATURDAY: "Сб",
            }
        }

        return translation[self.locale][self.day]
