from typing import Any, List

from aiogram.utils.json import json
from aioredis import Redis


async def student_preferences(user_id: int, redis: Redis) -> List[str]:
    res = await redis.get(name='student_preferences:' + str(user_id))
    # print(res)
    return json.loads(res.decode('utf-8'))


async def set_student_preferences(user_id: int, data: List[Any], redis: Redis):
    value = json.dumps(data, ensure_ascii=False)
    await redis.set(name='student_preferences:' + str(user_id), value=value, ex=3600 * 24)
