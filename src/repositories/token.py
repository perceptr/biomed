from dataclasses import asdict
from src.repositories.base import Repository
from src.models import Token
from src.schemas import TokenCreateSchema, TokenSchema


class TokenRepository(Repository[Token]):
    __model__ = Token

    async def create_token(self, schema: TokenCreateSchema) -> TokenSchema:
        """Создать запись о токене"""

        result = await self._create(**schema.model_dump())

        return TokenSchema.model_validate(result)

    async def get_token_by_value(self, token_value: str) -> TokenSchema | None:
        """Получить токен по значению"""

        result = await self._get(Token.value == token_value)

        return TokenSchema(**asdict(result)) if result else None

    async def set_token_status(self, token_value: str, *, is_active: bool) -> None:
        """Установить статус токена"""
        # todo если по логике удобнее получать через id, поменять на id

        await self._update(Token.value == token_value, is_active=is_active)
