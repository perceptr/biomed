from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.utils.utils import has_user_read_privacy_policy


class HasReadPrivacyPolicy(BaseFilter):
    def __init__(self) -> None:
        self.user_ids = 2

    async def __call__(self, message: Message) -> bool:
        # return message.from_user.id and has_user_read_privacy_policy()
        return True