from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)

async_sessionmaker_: async_sessionmaker[AsyncSession] | None = None


def get_async_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """DI for async_sessionmaker"""

    if async_sessionmaker_ is None:
        raise ValueError("async_sessionmaker_ wasn't initialised")

    return async_sessionmaker_
