from src.bot.db.dto import StatisticsResult
from src.bot.utils.utils import generate_token
from src.dependencies.db import get_async_sessionmaker, async_sessionmaker_
from src.repositories.analysis import AnalysisRepository
from src.repositories.operator import OperatorRepository
from src.repositories.statistics import StatisticsRepository
from src.repositories.token import TokenRepository
from src.repositories.user import UserRepository
from src.schemas import UserCreateSchema, AnalysisCreateSchema, TokenCreateSchema, OperatorCreateSchema, AnalysisSchema


async def create_user(telegram_id: int, **kwargs):
    async_sessionmaker_ = get_async_sessionmaker()
    user_repository = UserRepository(async_sessionmaker_)
    return await user_repository.create_user(
        UserCreateSchema(telegram_id=telegram_id, **kwargs)
    )


async def get_user_by_telegram_id(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    user_repository = UserRepository(async_sessionmaker_)
    return await user_repository.get_user_by_telegram_id(telegram_id)


async def send_analysis(telegram_id: int, **kwargs):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    user = await get_user_by_telegram_id(telegram_id)
    return await analysis_repository.create_analysis(
        AnalysisCreateSchema(user=user, **kwargs)
    )


async def is_user_created(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    user_repository = UserRepository(async_sessionmaker_)
    user = await user_repository.get_user_by_telegram_id(telegram_id)
    return user is not None


async def get_documents_by_user(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    user_repository = UserRepository(async_sessionmaker_)
    analyses = await user_repository.get_analyses_by_telegram_id(telegram_id)
    return analyses


async def create_token():
    async_sessionmaker_ = get_async_sessionmaker()
    token_repository = TokenRepository(async_sessionmaker_)
    token = await token_repository.create_token(
        TokenCreateSchema(
            is_active=True,
            value=generate_token()
        )
    )
    return token.value


async def get_token_by_value(token_value: str):
    async_sessionmaker_ = get_async_sessionmaker()
    token_repository = TokenRepository(async_sessionmaker_)
    token = await token_repository.get_token_by_value(token_value)
    return token if token and token.is_active else None


async def register_operator(telegram_id: int, token_value: str):
    token = await get_token_by_value(token_value)
    if token is None:
        return None

    async_sessionmaker_ = get_async_sessionmaker()
    operator_repository = OperatorRepository(async_sessionmaker_)

    existing_operator = await operator_repository.get_operator_by_token(token_value)
    if existing_operator is not None:
        return None

    operator = await operator_repository.create_operator(
        OperatorCreateSchema(telegram_id=telegram_id, token=token)
    )

    return operator


async def is_operator(telegram_id: int) -> bool:
    async_sessionmaker_ = get_async_sessionmaker()
    operator_repository = OperatorRepository(async_sessionmaker_)
    operator = await operator_repository.get_operator_by_telegram_id(telegram_id)
    if operator is not None:
        return operator.is_online
    return False


async def get_operator_by_tg_id(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    operator_repository = OperatorRepository(async_sessionmaker_)

    existing_operator = await operator_repository.get_operator_by_telegram_id(telegram_id)
    return existing_operator


async def count_uncompleted_analysis(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    operator = await get_operator_by_tg_id(telegram_id)
    count = await analysis_repository.get_uncompleted_analysis_count(operator.id)
    return count


async def set_operator_to_analysis(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    operator = await get_operator_by_tg_id(telegram_id)
    if operator is None:
        return None
    current_document = await analysis_repository.get_uncompleted_analysis_by_operator(operator.id)
    if current_document is not None:
        return current_document
    analysis = await analysis_repository.set_operator_to_oldest_uncompleted_analysis(operator.id)
    return analysis


async def unset_operator_to_analysis(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    operator = await get_operator_by_tg_id(telegram_id)
    await analysis_repository.unset_operator_from_analyses(operator.id)


async def finish_document(analysis_id: int, text: str):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    await analysis_repository.complete_analysis(analysis_id, text)


async def get_document(analysis_id: int) -> AnalysisSchema:
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    analysis = await analysis_repository.get_analysis_by_id(analysis_id)
    return analysis


async def delete_analysis(analysis_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    await analysis_repository.delete_analysis(analysis_id)


async def add_edit_note(analysis_id: int, note: str):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    await analysis_repository.set_edit_note(analysis_id, note)


async def change_doc_title(analysis_id: int, title: str):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    await analysis_repository.set_new_title(analysis_id, title)

async def logout_operator(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    operator_repository = OperatorRepository(async_sessionmaker_)
    operator = await operator_repository.get_operator_by_telegram_id(telegram_id)
    token_repository = TokenRepository(async_sessionmaker_)
    await operator_repository.set_operator_status(telegram_id, is_online=False)
    await unset_operator_to_analysis(telegram_id)
    await token_repository.set_token_status(operator.token.value, is_active=False)

async def login_or_create_operator(telegram_id: int, token_value: str):
    async_sessionmaker_ = get_async_sessionmaker()
    operator_repository = OperatorRepository(async_sessionmaker_)
    operator = await get_operator_by_tg_id(telegram_id)
    if operator is None:
        operator = await register_operator(telegram_id, token_value)
        return operator

    token = await get_token_by_value(token_value)
    if token is None:
        return None

    await operator_repository.set_operator_status(telegram_id, is_online=True)

    return operator


async def get_analysis_by_operator(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    operator = await get_operator_by_tg_id(telegram_id)
    result: AnalysisSchema | None = await analysis_repository.get_analysis_by_operator(operator.id)
    return result


async def get_statistics() -> StatisticsResult:
    async_sessionmaker_ = get_async_sessionmaker()
    statistics_repository = StatisticsRepository(async_sessionmaker_)

    return StatisticsResult(
        total_users=await statistics_repository.get_total_users(),
        total_operators=await statistics_repository.get_total_operators(),
        total_analyses=await statistics_repository.get_total_analyses(),
        analyses_status_counts=await statistics_repository.get_analyses_status_counts(),
        top_5_cities=await statistics_repository.get_top_5_cities(),
    )



