from src.bot.utils.utils import generate_token
from src.dependencies.db import get_async_sessionmaker, async_sessionmaker_
from src.repositories.analysis import AnalysisRepository
from src.repositories.operator import OperatorRepository
from src.repositories.token import TokenRepository
from src.repositories.user import UserRepository
from src.schemas import UserCreateSchema, AnalysisCreateSchema, TokenCreateSchema, OperatorCreateSchema


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
    print(operator)

    token_repository = TokenRepository(async_sessionmaker_)
    await token_repository.set_token_status(token_value, is_active=False)

    return operator


async def is_operator(telegram_id: int) -> bool:
    async_sessionmaker_ = get_async_sessionmaker()
    operator_repository = OperatorRepository(async_sessionmaker_)
    operator = await operator_repository.get_operator_by_telegram_id(telegram_id)
    return operator is not None


async def get_operator_by_tg_id(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    operator_repository = OperatorRepository(async_sessionmaker_)

    existing_operator = await operator_repository.get_operator_by_telegram_id(telegram_id)
    return existing_operator


async def count_uncompleted_analysis():
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    count = await analysis_repository.get_uncompleted_analysis_count()
    return count


async def set_operator_to_analysis(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    operator = await get_operator_by_tg_id(telegram_id)
    if operator is None:
        return None
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


async def get_document(analysis_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    analysis = await analysis_repository.get_analysis_by_id(analysis_id)
    return analysis
