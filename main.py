import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from contextlib import asynccontextmanager
from typing import AsyncIterator

import src.dependencies.db as db_module
from src.repositories.user import UserRepository
from src.settings import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT


@asynccontextmanager
async def lifespan() -> AsyncIterator[None]:
    db_url = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    async_engine = create_async_engine(db_url)
    async_sessionmaker_ = async_sessionmaker(async_engine)

    async with async_sessionmaker_() as session:
        await session.execute(select(1))

    print("Успешное соединение с базой!")

    db_module.async_sessionmaker_ = async_sessionmaker_

    yield

    await async_engine.dispose()


async def start_app():
    async_sessionmaker_ = db_module.get_async_sessionmaker()
    user_repository = UserRepository(async_sessionmaker_)

    founded_user = await user_repository.get_user_by_telegram_id(1234)

    print(founded_user)


async def main():
    async with lifespan():
        await start_app()


if __name__ == "__main__":
    asyncio.run(main())
