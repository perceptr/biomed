from src.repositories.base import Repository
from src.models import Tag, User, Analysis
from src.schemas import TagCreateSchema, TagSchema, UserSchema
from sqlalchemy import null, select, desc
from sqlalchemy.orm import joinedload


class TagRepository(Repository[Tag]):
    __model__ = Tag

    async def create_tag(
        self, schema: TagCreateSchema, user_id: int, analysis_id: int | None
    ) -> TagSchema:
        """Создать запись о токене"""
        async with self._get_session() as session:
            users = await session.execute(
                select(User).filter(User.id == user_id)
            )
            user = users.scalars().first()

            if user is None:
                raise ValueError("Илья, проеб")

            if analysis_id:
                analyses = await session.execute(
                    select(Analysis)
                    .options(joinedload(Analysis.user))
                    .where(Analysis.id == analysis_id)
                )
                analysis = analyses.scalars().first()

                if analysis is None:
                    raise ValueError("Илья, проеб дважды!")

            obj = Tag(
                user_id=user.id,
                name=schema.name,
                user=user,
                analyses=[analysis] if analysis_id else [],
                id=None, # noqa
            )

            session.add(obj)
            await session.commit()
            await session.refresh(obj)

            return TagSchema.model_validate(obj)

    async def get_tags(self, user_id: int) -> list[TagSchema]:
        """Получить тенге"""

        async with self._get_session() as session:
            result = await session.execute(
                select(Tag)
                .options(joinedload(Tag.user))
                .filter(Tag.user_id == user_id)
            )

            records = result.unique().scalars().all()

            return [TagSchema.model_validate(record) for record in records]

    async def delete_tag(self, tag_name: str, user_id: int) -> None:
        """Установить статус токена"""

        await self._delete(Tag.name == tag_name, Tag.user_id == user_id)
