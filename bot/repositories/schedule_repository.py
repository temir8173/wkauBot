from aioredis import Redis
from sqlalchemy.orm import sessionmaker


async def student_preferences(user_id: int, session_maker: sessionmaker, redis: Redis) -> bool:
    res = await redis.get(name='is_user_exists:' + str(user_id))
    print(res)
    return True