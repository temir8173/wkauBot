import aiohttp

from bot.config import SCHEDULE_API_OPTIONS_URL


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
