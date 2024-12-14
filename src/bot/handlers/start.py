from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from src.bot.answer_texts import START_ANSWER_TEXT
from src.bot.filters.has_read_privacy_policy import HasReadPrivacyPolicyFilter
from src.bot.filters.has_registered import HasRegisteredFilter
from src.bot.filters.is_operator import IsOperatorFilter
from src.bot.keyboards.main_menu import kb_main_menu
from src.bot.keyboards.operator_main_menu_kb import kb_operator_main_menu
from src.bot.keyboards.privacy_policy_kb import kb_privacy_policy
from src.bot.keyboards.register_kb import kb_register

start_router = Router()


@start_router.callback_query((F.data == "main_menu"),
    IsOperatorFilter(), HasReadPrivacyPolicyFilter()
)
async def cmd_operator_start(call: CallbackQuery):
    await call.message.answer("Выберите опцию:", reply_markup=kb_operator_main_menu())


@start_router.message(
    CommandStart(), IsOperatorFilter(), HasReadPrivacyPolicyFilter()
)
async def cmd_operator_start(message: Message):
    await message.answer("Выберите опцию:", reply_markup=kb_operator_main_menu())


@start_router.message(CommandStart(), ~HasReadPrivacyPolicyFilter())
async def user_has_not_read_privacy_policy(message: Message):
    await message.answer(START_ANSWER_TEXT, reply_markup=kb_privacy_policy())


@start_router.message(CommandStart(), ~HasRegisteredFilter())
async def user_has_not_registered(message: Message):
    await message.answer("Надо зарегистрироваться:", reply_markup=kb_register())


@start_router.message(
    CommandStart(), HasRegisteredFilter(), HasReadPrivacyPolicyFilter()
)
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    print(message.chat.id)
    await message.answer("Выберите опцию:", reply_markup=kb_main_menu())


@start_router.callback_query(F.data == "main_menu")
async def main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("Выберите опцию:", reply_markup=kb_main_menu())


@start_router.callback_query(F.data == "privacy_ok")
async def capture_privacy_policy_ok(call: CallbackQuery):
    await call.message.answer("Надо зарегистрироваться:", reply_markup=kb_register())
