from dataclasses import asdict
from src.repositories.base import Repository
from src.models import User, Analysis
from src.schemas import UserCreateSchema, UserSchema, AnalysisSchema
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class UserRepository(Repository[User]):
    __model__ = User

    async def create_user(self, schema: UserCreateSchema) -> UserSchema:
        """Создать запись о пользователе"""

        result = await self._create(**schema.model_dump())

        return UserSchema(**asdict(result))

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserSchema | None:
        """Получить запись о пользователе по telegram_id"""

        async with self._get_session() as session:
            result = await session.execute(
                select(User)
                .options(selectinload(User.analyses))
                .where(User.telegram_id == telegram_id)
            )
        user = result.scalars().first()

        if user is None:
            return None

        return UserSchema.model_validate(user)

    async def get_analyses_by_telegram_id(self, telegram_id: int) -> [AnalysisSchema]:
        """Получить список анализов пользователя по telegram_id"""

        async with self._get_session() as session:
            result = await session.execute(
                select(User)
                .options(selectinload(User.analyses))
                .where(User.telegram_id == telegram_id)
            )
            user = result.scalars().first()

        if user is None:
            raise ValueError(f"Пользователь с telegram_id {telegram_id} не найден.")

        return [AnalysisSchema.model_validate(analysis) for analysis in user.analyses]

        # user = await self._get(User.telegram_id == telegram_id)
        #
        # if user is None:
        #     raise ValueError(f"Шлем этого пользователя в пизду {telegram_id}")
        #
        # async with self._get_session() as session:
        #     result = await session.execute(
        #         select(Analysis)
        #         .where(Analysis.user_id == user.id)
        #     )
        #     records = result.scalars().unique()
        #
        # # return AnalysisSchema.model_validate(record) if record else None
        #
        # return [AnalysisSchema(**asdict(analysis)) for analysis in records]
