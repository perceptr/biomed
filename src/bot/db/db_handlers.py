from src.dependencies.db import get_async_sessionmaker
from src.repositories.analysis import AnalysisRepository
from src.repositories.user import UserRepository
from src.schemas import UserCreateSchema, AnalysisCreateSchema

async def create_user(telegram_id: int, **kwargs):
    async_sessionmaker_ = get_async_sessionmaker()
    user_repository = UserRepository(async_sessionmaker_)
    return await user_repository.create_user(
        UserCreateSchema(telegram_id=telegram_id, **kwargs))


async def send_analysis(telegram_id: int, **kwargs):
    async_sessionmaker_ = get_async_sessionmaker()
    user_repository = UserRepository(async_sessionmaker_)
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    user = await user_repository.get_user_by_telegram_id(telegram_id)
    return await analysis_repository.create_analysis(
        AnalysisCreateSchema(user=user, **kwargs))


async def is_user_created(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    user_repository = UserRepository(async_sessionmaker_)
    analysis_repository = AnalysisRepository(async_sessionmaker_)
    user = await user_repository.get_user_by_telegram_id(telegram_id)
    return user is not None


async def get_documents_by_user(telegram_id: int):
    async_sessionmaker_ = get_async_sessionmaker()
    user_repository = UserRepository(async_sessionmaker_)
    analyses = await user_repository.get_analyses_by_telegram_id(telegram_id)
    return analyses

