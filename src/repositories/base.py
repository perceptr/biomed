from contextlib import asynccontextmanager
from typing import Any, Generic, TypeVar, AsyncIterator

from sqlalchemy import ColumnElement, delete, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.models import Base

T = TypeVar("T", bound=Base)


class Repository(Generic[T]):
    """Базовый репозиторий"""

    __model__: type[T]

    def __init__(self, async_sessionmaker_: async_sessionmaker[AsyncSession]) -> None:
        self._async_sessionmaker = async_sessionmaker_

    @asynccontextmanager
    async def _get_session(self) -> AsyncIterator[AsyncSession]:
        async with self._async_sessionmaker() as session:
            yield session

    async def _create(self, **values: Any) -> T:
        async with self._get_session() as session:
            value = self.__model__(**values)
            session.add(value)
            await session.commit()
            return value

    async def _delete(self, *filters: ColumnElement[bool]) -> None:
        async with self._get_session() as session:
            await session.execute(delete(self.__model__).filter(*filters))
            await session.commit()

    async def _get_all(self, *filters: ColumnElement[bool]) -> list[T]:
        async with self._get_session() as session:
            records = await session.execute(select(self.__model__).filter(*filters))

            return list(records.scalars().all())

    async def _get(self, *filters: ColumnElement[bool]) -> T | None:
        async with self._get_session() as session:
            records = await session.execute(select(self.__model__).filter(*filters))

            return records.scalars().first()

    async def _update(
        self, *filters: ColumnElement[bool], **values: Any
    ) -> None:
        async with self._get_session() as session:
            await session.execute(
                update(self.__model__).filter(*filters).values(**values)
            )
            await session.commit()
