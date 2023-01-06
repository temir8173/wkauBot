from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikbTest = InlineKeyboardMarkup(width=2)
ibTest = InlineKeyboardButton(text='button1', url='https://stackoverflow.com/questions/54297615/docker-exec-linux-terminal-create-alias')
ibTestSec = InlineKeyboardButton(text='button2', url='https://www.google.com')

ikbTest.add(ibTest).add(ibTestSec)

