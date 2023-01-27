from typing import Dict, Any

import aiohttp

from bot.config import SCHEDULE_API_OPTIONS_URL, SCHEDULE_API_SCHEDULE_URL


async def get_options(parent_option_id: int = None, target: str = 'institute') -> list:
    async with aiohttp.ClientSession() as session:
        async with session.post(SCHEDULE_API_OPTIONS_URL, data={
            'id': parent_option_id,
            'target': target
        }) as response:
            return await response.json()


async def get_option_value(option_id: int, parent_option_id: int = None, target: str = 'institute') -> str:
    options = await get_options(parent_option_id, target)
    for option in options:
        if option['id'] == option_id:
            return option['value']


async def get_schedule(institute: int, school: int, group: int, week: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.post(SCHEDULE_API_SCHEDULE_URL, data={
            'institute': institute,
            'school': school,
            'group': group,
            'week': week
        }) as response:
            return await response.json()


async def get_schedule_for_teacher(institute: int, school: int, teacher: int, week: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.post(SCHEDULE_API_SCHEDULE_URL, data={
            'institute': institute,
            'school': school,
            'teacher': teacher,
            'week': week
        }) as response:
            return await response.json()
