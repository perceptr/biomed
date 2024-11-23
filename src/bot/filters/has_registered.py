from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.db import is_user_created


class HasRegisteredFilter(BaseFilter):
    def __init__(self) -> None:
        return

    async def __call__(self, message: Message) -> bool:
        has_registered = await is_user_created(message.from_user.id)
        return has_registered
