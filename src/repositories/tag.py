from dataclasses import asdict
from src.repositories.base import Repository
from src.models import Tag
from src.schemas import TagCreateSchema, TagSchema, UserSchema


class TagRepository(Repository[Tag]):
    __model__ = Tag

    async def create_tag(
        self, schema: TagCreateSchema, user_schema: UserSchema
    ) -> TagSchema:
        """Создать запись о токене"""

        result = await self._create(**schema.model_dump(), user_id=user_schema.id)

        return TagSchema(**asdict(result))

    async def get_tag(self, tag_name: str, user_schema: UserSchema) -> TagSchema | None:
        """Получить тэг"""

        result = await self._get(Tag.name == tag_name, Tag.user_id == user_schema.id)

        return TagSchema(**asdict(result)) if result else None

    async def delete_tag(self, tag_name: str, user_schema: UserSchema) -> None:
        """Установить статус токена"""

        await self._delete(Tag.name == tag_name, Tag.user_id == user_schema.id)
