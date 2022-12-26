from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

class CustomMiddleware(BaseMiddleware):
    async def on_preprocess_update(self, update: types.Update, data: dict):
        print('Pre process update')

    async def on_process_update(self, update: types.Update, data: dict):
        print('Process update')

