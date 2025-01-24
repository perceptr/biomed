from src.dependencies.db import get_async_sessionmaker
from src.repositories.analysis import AnalysisRepository
from src.schemas import OperatorSchema
from src.bot.create_bot import bot


async def task_revoke_expired_analyses() -> dict[OperatorSchema, str]:
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)

    expired_analyses = await analysis_repository.get_expired_analyses()
    await analysis_repository.revoke_assigned_operators([analysis.id for analysis in expired_analyses])

    operator_analysis_map = {exp.assigned_operator: exp.name for exp in expired_analyses}

    for operator, analysis_name in operator_analysis_map.items():
        if operator and operator.telegram_id:
            await bot.send_message(
                chat_id=operator.telegram_id,
                text=f"Извините, время для расшифровки анализа {analysis_name} истекло. Анализ"
                     f" снова доступен для обработки всем свободным операторам",
            )

    await analysis_repository.revoke_assigned_operators([analysis.id for analysis in expired_analyses])
    return operator_analysis_map
