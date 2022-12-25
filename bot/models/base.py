"""
    Базовые классы базы данных
"""
#  Copyright (c) 2022.

from abc import abstractmethod
from datetime import timedelta, datetime as dt

from sqlalchemy import Column, DateTime, Integer  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore


class CleanModel:
    created_at = Column(DateTime, default=dt.now())
    updated_at = Column(DateTime, onupdate=dt.now())

    @property
    def no_upd_time(self) -> timedelta:
        """
        Получить время, которое модель не обновлялась
        :return: timedelta
        """
        return self.updated_at - dt.now()  # type: ignore


class Model(CleanModel):
    """
        Базовая бизнес-модель в базе данных
    """
    @property
    @abstractmethod
    def stats(self) -> str:
        """
        Функция для обработки и получения в строковом формате
        статистики модели (пользователя, ссылки, поста или канала)
        :return:
        """
        ...


Base = declarative_base(cls=Model)
