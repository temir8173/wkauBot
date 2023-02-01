from typing import Union

from redis.asyncio.client import Redis
from sqlalchemy import Column, Integer, VARCHAR, select, BigInteger, Enum, update  # type: ignore
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker, relationship, selectinload  # type: ignore

from bot.models.base import Base
from bot.models.user import User


async def get_user(user_id: int, session_maker: sessionmaker) -> Union[User, None]:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                .filter(User.user_id == user_id)  # type: ignore
            )
            return result.scalars().one_or_none()


async def update_locale(user_id, locale: str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(Base.metadata.tables[User.__tablename__])
                                  .values(locale=locale)
                                  .where(User.user_id == user_id))


async def create_user(user_id: int, username: str, locale: str, session_maker: sessionmaker, redis: Redis) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=username
            )
            try:
                session.add(user)
                await set_user_exist(user_id=user_id, redis=redis, value=1)
                await session.commit()
            except ProgrammingError as e:
                # TODO: add log
                pass


async def is_user_exists(user_id: int, session_maker: sessionmaker, redis: Redis) -> bool:
    res = await redis.get(name='is_user_exists:' + str(user_id))
    if not res or not bool(int(res)):
        async with session_maker() as session:
            async with session.begin():
                sql_res = await session.execute(select(User).where(User.user_id == user_id))
                user = sql_res.scalar_one_or_none()
                await set_user_exist(user_id=user_id, redis=redis, value=1 if user else 0)
                return bool(user)
    else:
        return bool(int(res))


async def set_user_exist(user_id: int, redis: Redis, value: int = 1):
    await redis.set(name='is_user_exists:' + str(user_id), value=value, ex=3600 * 24)
