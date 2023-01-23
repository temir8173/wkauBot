from aiogram import Dispatcher

from . import errors
from . import user
from . import schedule_options


def setup(dp: Dispatcher):
    schedule_options.setup(dp)
    errors.setup(dp)
    user.setup(dp)
