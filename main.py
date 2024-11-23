import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import src.dependencies.db as db_module
from src.bot.forms.upload_document import upload_document_router
from src.bot.forms.user_form import user_info_router
from src.bot.handlers.edit_docuents import edit_documents_router
from src.bot.handlers.list_documents import list_documents_router
from src.bot.handlers.start import start_router
from src.settings import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT
from src.bot.create_bot import bot, dp


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
    async_sessionmaker_ = db_module.get_async_sessionmaker()  # noqa
    dp.include_router(start_router)
    dp.include_router(user_info_router)
    dp.include_router(upload_document_router)
    dp.include_router(list_documents_router)
    dp.include_router(edit_documents_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main():
    async with lifespan():
        await start_app()


if __name__ == "__main__":
    asyncio.run(main())
