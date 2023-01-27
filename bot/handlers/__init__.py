from aiogram import Dispatcher

from . import errors
from . import user
from . import student_schedule
from . import teacher_schedule


def setup(dp: Dispatcher):
    student_schedule.setup(dp)
    teacher_schedule.setup(dp)
    errors.setup(dp)
    user.setup(dp)
