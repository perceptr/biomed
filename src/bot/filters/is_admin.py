from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.settings import ADMINS


class IsAdminFilter(BaseFilter):
    def __init__(self) -> None:
        self.user_ids = set(ADMINS)

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.user_ids
