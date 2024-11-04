from src.repositories.base import Repository
from src.models import Token
from src.schemas import TokenSchema


class TokenRepository(Repository[Token]):
    __model__ = Token

    async def create_token(self, schema: TokenSchema) -> None:
        """Создать запись о токене"""

        await self._create(**schema.model_dump())

    async def get_token_by_value(self, token_value: str) -> TokenSchema | None:
        """Получить токен по значению"""

        result = await self._get(Token.value == token_value)

        if result is None:
            return None

        return TokenSchema.model_validate(result)

    async def set_token_status(self, token_value: str, *, is_active: bool) -> None:
        """Установить статус токена"""

        await self._update(Token.value == token_value, is_active=is_active)
