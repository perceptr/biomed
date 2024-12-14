from dataclasses import asdict
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.base import Repository
from src.models import Operator, Token
from src.schemas import OperatorCreateSchema, OperatorSchema


class OperatorRepository(Repository[Operator]):
    __model__ = Operator

    async def create_operator(self, schema: OperatorCreateSchema) -> OperatorSchema:
        """Создать запись об операторе"""
        async with self._get_session() as session:
            records = await session.execute(
                select(Token).filter(Token.id == schema.token.id)
            )
            record = records.scalars().first()
            if record is None:
                raise ValueError("Pizda")

            values = schema.model_dump(exclude={"token"})
            values["token"] = record

            new_obj = Operator(**values, token_id=schema.token.id)
            session.add(new_obj)
            await session.commit()
            await session.refresh(new_obj)

            return OperatorSchema.model_validate(new_obj)

    async def get_operator_by_telegram_id(
        self, telegram_id: int
    ) -> OperatorSchema | None:
        """Получить запись об операторе по telegram_id"""

        async with self._get_session() as session:
            result = await session.execute(
                select(Operator)
                .options(selectinload(Operator.analyses))
                .filter(Operator.telegram_id == telegram_id)
            )

        operator = result.scalars().first()

        if operator is None:
            return None

        return OperatorSchema.model_validate(operator)

    async def get_operator_by_token(self, token_value: str) -> OperatorSchema | None:
        """Получить запись об операторе по токену"""

        async with self._get_session() as session:
            records = await session.execute(
                select(Operator).join(Operator.token).filter(Token.value == token_value)
            )
            result = records.scalars().first()

            return OperatorSchema.model_validate(result) if result else None

    async def set_operator_status(self, telegram_id: int, *, is_online: bool) -> None:
        """Установить статус оператора"""

        await self._update(Operator.telegram_id == telegram_id, is_online=is_online)
