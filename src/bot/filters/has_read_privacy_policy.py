import random

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.db import is_user_created


class HasReadPrivacyPolicyFilter(BaseFilter):
    def __init__(self) -> None:
        self.user_ids = 2

    async def __call__(self, message: Message) -> bool:
        return True
        # has_registered = await is_user_created(message.from_user.id)

        # return has_registered
