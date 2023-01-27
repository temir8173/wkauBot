from typing import Any, List

from aiogram.utils.json import json
from aioredis import Redis


async def student_preferences(user_id: int, redis: Redis) -> List[str]:
    res = await redis.get(name='student_preferences:' + str(user_id))
    return [] if res is None else json.loads(res.decode('utf-8'))


async def set_student_preferences(user_id: int, data: List[Any], redis: Redis):
    value = json.dumps(data, ensure_ascii=False)
    await redis.set(name='student_preferences:' + str(user_id), value=value, ex=3600 * 24)


async def teacher_preferences(user_id: int, redis: Redis) -> List[str]:
    res = await redis.get(name='teacher_preferences:' + str(user_id))
    return [] if res is None else json.loads(res.decode('utf-8'))


async def set_teacher_preferences(user_id: int, data: List[Any], redis: Redis):
    value = json.dumps(data, ensure_ascii=False)
    await redis.set(name='teacher_preferences:' + str(user_id), value=value, ex=3600 * 24)
