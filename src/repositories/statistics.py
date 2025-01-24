from typing import List, Tuple, Dict
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User, Operator, Analysis


class StatisticsRepository:
    def __init__(self, async_sessionmaker):
        self.async_sessionmaker = async_sessionmaker

    async def get_total_users(self) -> int:
        async with self.async_sessionmaker() as session:  # type: AsyncSession
            result = await session.execute(
                select(func.count(User.id))
            )
            return result.scalar_one()

    async def get_total_operators(self) -> int:
        async with self.async_sessionmaker() as session:
            result = await session.execute(
                select(func.count(Operator.id))
            )
            return result.scalar_one()

    async def get_total_analyses(self) -> int:
        async with self.async_sessionmaker() as session:
            result = await session.execute(
                select(func.count(Analysis.id))
            )

            return result.scalar_one()

    async def get_analyses_status_counts(self) -> Dict[str, int]:
        async with self.async_sessionmaker() as session:
            result = await session.execute(
                select(
                    Analysis.status,
                    func.count(Analysis.id)
                ).group_by(Analysis.status)
            )
            rows = result.all()

            return {status.value: count for status, count in rows}

    async def get_top_5_cities(self) -> List[Tuple[str, int]]:
        async with self.async_sessionmaker() as session:
            result = await session.execute(
                select(
                    User.city,
                    func.count(User.id).label("user_count")
                )
                .group_by(User.city)
                .order_by(desc("user_count"))
                .limit(5)
            )
            return result.all()
