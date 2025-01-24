import random
from functools import lru_cache

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.db import is_user_created

READ_PRIVACY_POLICY = set()


class HasReadPrivacyPolicyFilter(BaseFilter):
    def __init__(self) -> None:
        self.user_ids = 2

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in READ_PRIVACY_POLICY