from aiogram import Router, F
from aiogram.types import CallbackQuery
from src.bot.db.db_handlers import logout_operator
from src.bot.filters.is_operator import IsOperatorFilter
from src.bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from aiogram.utils.chat_action import ChatActionSender
from src.bot.create_bot import bot

logout_operator_router = Router()

@logout_operator_router.callback_query(F.data.startswith("quit_operator"))
async def logout_operator_handler(call: CallbackQuery):
    await call.answer()
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await logout_operator(call.from_user.id)
        await call.message.answer(
            "Вы вышли из аккаунта оператора. Чтобы зайти обратно, воспользуйтесь тем же токеном.",
            reply_markup=kb_back_to_main_menu(),
        )