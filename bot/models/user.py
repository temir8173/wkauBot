"""
    Модель пользователя
"""
#  Copyright (c) 2022.

from sqlalchemy import Column, Integer, VARCHAR, select, BigInteger, Enum
from sqlalchemy.orm import sessionmaker, relationship, selectinload

from .base import Base # type: ignore


class User(Base):
    __tablename__ = 'users'

    # Telegram user id
    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    # balance = Column(Integer, default=0)
    locale = Column(VARCHAR(2), default='kz')

    @property
    def stats(self) -> str:
        return ""

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()
