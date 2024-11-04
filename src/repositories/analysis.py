from asyncio import Semaphore
from dataclasses import asdict
from sqlalchemy import null, select

from src.repositories.base import Repository
from src.models import Analysis
from src.schemas import (
    AnalysisCreateSchema,
    AnalysisSchema,
    AnalysisStatusEnum,
    OperatorSchema,
    UserSchema,
)

_mutex = Semaphore(1)


class AnalysisRepository(Repository[Analysis]):
    __model__ = Analysis

    async def create_analysis(
        self, schema: AnalysisCreateSchema, user_schema: UserSchema
    ) -> AnalysisSchema:
        """Создать анализ"""

        result = await self._create(**schema.model_dump(), user_id=user_schema.id)

        return AnalysisSchema(**asdict(result))

    async def get_analysis_by_id(self, analysis_id: int) -> AnalysisSchema | None:
        """ Получить анализ по id """

        result = await self._get(Analysis.id == analysis_id)

        return AnalysisSchema(**asdict(result)) if result else None

    async def get_analysis_by_operator(
        self, operator: OperatorSchema
    ) -> AnalysisSchema | None:
        """ Получить анализ по присвоенному оператору """

        result = await self._get(Analysis.assigned_operator_id == operator.id)

        return AnalysisSchema(**asdict(result)) if result else None

    async def _get_oldest_uncomplited_analysis(self) -> AnalysisSchema | None:
        async with self._get_session() as session:
            records = await session.execute(
                select(Analysis)
                .filter(Analysis.assigned_operator_id == null)
                .order_by(Analysis.created_at.asc())
            )

            result = records.scalars().first()

            return AnalysisSchema(**asdict(result)) if result else None

    async def _set_operator_to_analysis(
        self, analysis_id: int, operator_id: int
    ) -> None:

        await self._update(Analysis.id == analysis_id, operator_id=operator_id)

    async def unset_operator_from_analyses(self, operator: OperatorSchema):
        """Удаляет оператора со всех незавершенных анализов"""

        await self._update(
            Analysis.assigned_operator_id == operator.id,
            Analysis.status != AnalysisStatusEnum.completed,
        )

    async def complete_analysis(self, analysis_id: int, result_text: str):
        """Завершить работу с анализом"""

        await self._update(
            Analysis.id == analysis_id,
            status=AnalysisStatusEnum.completed,
            result=result_text,
        )

    async def set_operator_to_oldest_uncomplited_analysis(
        self,
        operator: OperatorSchema,
    ) -> AnalysisSchema | None:
        """Устанавливает переданного оператора на самый старый анализ"""

        async with _mutex:
            analysis = await self._get_oldest_uncomplited_analysis()

            if analysis is None:
                return None

            await self._set_operator_to_analysis(analysis.id, operator.id)

            return await self._get(analysis.id)
