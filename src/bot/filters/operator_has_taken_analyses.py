from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.db.db_handlers import is_operator, count_uncompleted_analysis, get_analysis_by_operator


class IsOperatorFree(BaseFilter):
    def __init__(self) -> None:
        return

    async def __call__(self, message: Message) -> bool:
        analysis = await get_analysis_by_operator(message.from_user.id)
        return analysis is None or analysis.status == "completed"