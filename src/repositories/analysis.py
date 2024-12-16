from asyncio import Semaphore
from sqlalchemy import null, select, desc
from sqlalchemy.orm import joinedload

from src.repositories.base import Repository
from src.models import Analysis, User, Tag
from src.schemas import (
    AnalysisCreateSchema,
    AnalysisSchema,
    AnalysisStatusEnum,
)

_mutex = Semaphore(1)


class AnalysisRepository(Repository[Analysis]):
    __model__ = Analysis

    async def create_analysis(self, schema: AnalysisCreateSchema) -> AnalysisSchema:
        """Создать анализ"""
        async with self._get_session() as session:
            records = await session.execute(
                select(User).filter(User.id == schema.user.id)
            )
            record = records.scalars().first()
            if record is None:
                raise ValueError("Илья, проеб")

            obj = Analysis(
                **schema.model_dump(exclude={"user"}),
                user=record,
                user_id=schema.user.id,
                assigned_operator_id=None,
            )
            session.add(obj)
            await session.commit()
            await session.refresh(obj)

            return AnalysisSchema.model_validate(obj)

    async def get_analysis_by_id(self, analysis_id: int) -> AnalysisSchema | None:
        """Получить анализ по id"""

        # result = await self._get(Analysis.id == analysis_id)
        async with self._get_session() as session:
            result = await session.execute(
                select(Analysis)
                .options(joinedload(Analysis.user))
                .where(Analysis.id == analysis_id)
            )
            record = result.scalars().first()

            return AnalysisSchema.model_validate(record) if record else None

    async def get_analysis_by_operator(self, operator_id: int) -> AnalysisSchema | None:
        """Получить анализ по присвоенному оператору"""

        async with self._get_session() as session:
            result = await session.execute(
                select(Analysis)
                .options(
                    joinedload(Analysis.user), joinedload(Analysis.assigned_operator)
                )
                .where(Analysis.assigned_operator_id == operator_id)
            )
            record = result.scalars().first()

            return AnalysisSchema.model_validate(record) if record else None

    async def _get_oldest_uncompleted_analysis(self) -> AnalysisSchema | None:
        async with self._get_session() as session:
            records = await session.execute(
                select(Analysis)
                .options(joinedload(Analysis.user))
                .filter(Analysis.assigned_operator_id == null())
                .order_by(desc(Analysis.created_at))
            )

            result = records.scalars().first()

            return AnalysisSchema.model_validate(result) if result else None

    async def _set_operator_to_analysis(
        self, analysis_id: int, operator_id: int
    ) -> None:
        await self._update(Analysis.id == analysis_id, assigned_operator_id=operator_id)

    async def unset_operator_from_analyses(self, operator_id: int):
        """Удаляет оператора со всех незавершенных анализов"""

        await self._update(
            Analysis.assigned_operator_id == operator_id,
            Analysis.status != AnalysisStatusEnum.completed,
            assigned_operator_id=None,
        )

    async def complete_analysis(self, analysis_id: int, result_text: str):
        """Завершить работу с анализом"""

        await self._update(
            Analysis.id == analysis_id,
            status=AnalysisStatusEnum.completed,
            result=result_text,
        )

    async def set_operator_to_oldest_uncompleted_analysis(
        self,
        operator_id: int,
    ) -> AnalysisSchema | None:
        """Устанавливает переданного оператора на самый старый анализ"""

        async with _mutex:
            analysis = await self._get_oldest_uncompleted_analysis()

            if analysis is None:
                return None

            await self._set_operator_to_analysis(analysis.id, operator_id)

            return AnalysisSchema.model_validate(analysis)

    async def get_uncompleted_analysis_count(self) -> int:
        async with self._get_session() as session:
            records = await session.execute(
                select(Analysis)
                .options(joinedload(Analysis.user))
                .filter(Analysis.assigned_operator_id == null())
            )
        return len(records.scalars().unique().all())

    async def set_edit_note(self, analysis_id: int, edit_note: str) -> None:
        await self._update(Analysis.id == analysis_id, edit_note=edit_note, status=AnalysisStatusEnum.in_progress)

    async def delete_analysis(self, analysis_id: int) -> None:
        await self._delete(Analysis.id == analysis_id)

    async def get_analyses_by_tag(self, tag_name: str, user_id: int) -> list[AnalysisSchema]:
        """Получить по ебалу"""

        async with self._get_session() as session:
            result = await session.execute(
                select(Analysis)
                .join(Analysis.tags)
                .options(joinedload(Analysis.user), joinedload(Analysis.tags))
                .where(Tag.name == tag_name, Tag.user_id == user_id)
            )

            records = result.unique().scalars().all()

            return [AnalysisSchema.model_validate(record) for record in records]

    async def remove_tag_from_analysis(self, tag_name: str, analysis_id: int) -> None:
        async with self._get_session() as session:
            result = await session.execute(
                select(Analysis)
                .options(joinedload(Analysis.tags))
                .where(Analysis.id == analysis_id)
            )

            analysis = result.scalars().first()

            if analysis is None:
                return

            new_tags = [tag for tag in analysis.tags if tag.name != tag_name]

            if len(new_tags) == len(analysis.tags):
                return

            analysis.tags = new_tags
            await session.commit()
