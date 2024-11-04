from src.repositories.base import Repository
from src.models import Operator
from src.schemas import OperatorCreateSchema, OperatorSchema, TokenSchema


class OperatorRepository(Repository[Operator]):
    __model__ = Operator

    async def create_operator(
        self, schema: OperatorCreateSchema, token: TokenSchema
    ) -> OperatorSchema:
        """Создать запись об операторе"""

        result = await self._create(**schema.model_dump(), token_id=token.id)

        return OperatorSchema.model_validate(result)

    async def get_operator_by_telegram_id(
        self, telegram_id: int
    ) -> OperatorSchema | None:
        """Получить запись об операторе по telegram_id"""

        found_operator = await self._get(Operator.telegram_id == telegram_id)

        if not found_operator:
            return None

        return OperatorSchema.model_validate(found_operator)

    async def get_operator_by_token(self, token_value: str) -> OperatorSchema | None:
        """Получить запись об операторе по токену"""

        found_operator = await self._get(Operator.token.value == token_value)

        if not found_operator:
            return None

        return OperatorSchema.model_validate(found_operator)

    async def set_operator_status(self, telegram_id: int, *, is_active: bool) -> None:
        """Установить статус оператора"""

        await self._update(Operator.telegram_id == telegram_id, is_active=is_active)
