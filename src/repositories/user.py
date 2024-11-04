from src.repositories.base import Repository
from src.models import User
from src.schemas import UserCreateSchema, UserSchema


class UserRepository(Repository[User]):
    __model__ = User

    async def create_user(self, schema: UserCreateSchema) -> UserSchema:
        """Создать запись о пользователе"""

        result = await self._create(**schema.model_dump())

        return UserSchema.model_validate(result)

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserSchema | None:
        """Получить запись о пользователе по telegram_id"""

        found_user = await self._get(User.telegram_id == telegram_id)

        if not found_user:
            return None

        return UserSchema.model_validate(found_user)
