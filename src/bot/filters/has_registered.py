from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.db import is_user_created
from src.bot.db.db_handlers import get_operator_by_tg_id, is_operator


class HasRegisteredFilter(BaseFilter):
    def __init__(self) -> None:
        return

    async def __call__(self, message: Message) -> bool:
        has_registered = await is_user_created(message.from_user.id)
        has_registered_as_operator = await is_operator(message.from_user.id)
        return has_registered or has_registered_as_operator
