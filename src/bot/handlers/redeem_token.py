from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from src.bot.answer_texts import START_ANSWER_TEXT
from src.bot.create_bot import bot
from src.bot.db.db_handlers import get_user_by_telegram_id, register_operator, login_or_create_operator
from src.bot.filters.has_read_privacy_policy import HasReadPrivacyPolicyFilter
from src.bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from src.bot.keyboards.edit_docuemnts_kb import kb_edit_document
from src.bot.keyboards.list_documents_kb import kb_list_edit_documents
from src.bot.keyboards.main_menu import kb_main_menu
from mocks.documents import get_mock_documents
from src.bot.keyboards.privacy_policy_kb import kb_privacy_policy

redeem_token_router = Router()

class RedeemToken(StatesGroup):
    token = State()

# @redeem_token_router.callback_query((F.data == "register_operator"), ~HasReadPrivacyPolicyFilter())
async def has_not_read_privacy_policy(message: Message):
    await message.answer(START_ANSWER_TEXT, reply_markup=kb_privacy_policy())


redeem_token_router.callback_query.register(has_not_read_privacy_policy, F.data == "register_operator", ~HasReadPrivacyPolicyFilter())
redeem_token_router.message.register(has_not_read_privacy_policy, Command("login_operator"), ~HasReadPrivacyPolicyFilter())


@redeem_token_router.callback_query((F.data == "register_operator"), HasReadPrivacyPolicyFilter())
async def redeem_token(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await call.message.answer("Введите токен:")
    await state.set_state(RedeemToken.token)


@redeem_token_router.message(Command("login_operator"), HasReadPrivacyPolicyFilter())
async def redeem_token(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer("Введите токен:")
    await state.set_state(RedeemToken.token)


@redeem_token_router.message(F.text, RedeemToken.token)
async def check_token(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        operator = await login_or_create_operator(message.from_user.id, message.text)
        if operator is None:
            await message.answer("Токен недействителен")
        else:
            await message.answer(
                "Успешная авторизация!",
                reply_markup=kb_back_to_main_menu(),
            )
        await state.clear()
