from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.db.db_handlers import is_operator, count_uncompleted_analysis


class IsAnyAnalysesNotReady(BaseFilter):
    def __init__(self) -> None:
        return

    async def __call__(self, message: Message) -> bool:
        analyses_count = await count_uncompleted_analysis(message.from_user.id)
        return analyses_count != 0