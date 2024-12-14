from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.db.db_handlers import is_operator


class IsOperatorFilter(BaseFilter):
    def __init__(self) -> None:
        return

    async def __call__(self, message: Message) -> bool:
        is_oper = await is_operator(message.from_user.id)
        return is_oper