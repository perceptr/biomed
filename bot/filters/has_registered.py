from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.utils.utils import is_user_registered

counter = 0

class HasRegistered(BaseFilter):
    def __init__(self) -> None:
        self.user_ids = 2

    async def __call__(self, message: Message) -> bool:
        global counter
        counter += 1
        # return message.from_user.id and is_user_registered()
        # return counter % 2 == 0
        return True