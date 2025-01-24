from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from src.bot.answer_texts import START_ANSWER_TEXT
from src.bot.create_bot import bot
from src.bot.db.db_handlers import create_token, get_statistics
from src.bot.filters.has_read_privacy_policy import HasReadPrivacyPolicyFilter
from src.bot.filters.has_registered import HasRegisteredFilter
from src.bot.filters.is_admin import IsAdminFilter
from aiogram.types.callback_query import CallbackQuery

from src.bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from src.bot.keyboards.privacy_policy_kb import kb_privacy_policy
from src.bot.keyboards.register_kb import kb_register

create_token_router = Router()


@create_token_router.message(Command("create_token"), ~IsAdminFilter())
async def not_admin(message: Message):
    return


@create_token_router.callback_query(Command("create_token"), ~HasReadPrivacyPolicyFilter())
async def has_not_read_privacy_policy(message: Message):
    await message.answer(START_ANSWER_TEXT, reply_markup=kb_privacy_policy())


@create_token_router.callback_query(Command("create_token"), ~HasRegisteredFilter())
async def user_has_not_registered(message: Message):
    await message.answer("Надо зарегистрироваться:", reply_markup=kb_register())


@create_token_router.message(Command("create_token"), IsAdminFilter())
async def cmd_create_token(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        token = await create_token()
        await message.answer(
            f"Сгенерированный токен: {token}",
            reply_markup=kb_back_to_main_menu(),
        )


@create_token_router.message(Command("stats"), IsAdminFilter())
async def cmd_get_stats(message: Message):
    statistics = await get_statistics()
    top_cities = "\n".join([f"{i + 1}. {statistics.top_5_cities[i][0] } - {statistics.top_5_cities[i][1]}" for i in range(len(statistics.top_5_cities))])

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer(
            f"У нас {statistics.total_users} пользователей, "
            f"{statistics.total_operators} операторов, всего {statistics.total_analyses} документов, "
            f"из них обработали {statistics.analyses_status_counts['completed']}, в работе {statistics.analyses_status_counts['in_progress']}.\n\nНаши самые популярные города:\n{top_cities}",
            reply_markup=kb_back_to_main_menu(),
        )
