from dataclasses import asdict
from src.repositories.base import Repository
from src.models import User
from src.schemas import UserCreateSchema, UserSchema


class UserRepository(Repository[User]):
    __model__ = User

    async def create_user(self, schema: UserCreateSchema) -> UserSchema:
        """Создать запись о пользователе"""

        result = await self._create(**schema.model_dump())

        return UserSchema(**asdict(result))

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserSchema | None:
        """Получить запись о пользователе по telegram_id"""

        result = await self._get(User.telegram_id == telegram_id)

        return UserSchema(**asdict(result)) if result else None
