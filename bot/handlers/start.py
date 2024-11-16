from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.answer_texts import START_ANSWER_TEXT
from bot.filters.has_read_privacy_policy import HasReadPrivacyPolicy
from bot.filters.has_registered import HasRegistered
from bot.keyboards.main_menu import kb_main_menu
from bot.keyboards.privacy_policy_kb import kb_privacy_policy
from bot.keyboards.register_kb import kb_register

start_router = Router()


@start_router.message(CommandStart(), ~HasReadPrivacyPolicy())
async def user_has_not_read_privacy_policy(message: Message):
    await message.answer(
        START_ANSWER_TEXT,
        reply_markup=kb_privacy_policy()
    )


@start_router.message(CommandStart(), ~HasRegistered())
async def user_has_not_registered(message: Message):
    await message.answer(
        "Надо зарегистрироваться:",
        reply_markup=kb_register()
    )

@start_router.message(CommandStart(), HasRegistered(), HasReadPrivacyPolicy())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Выберите опцию:",
        reply_markup=kb_main_menu()
    )


@start_router.callback_query(F.data == 'main_menu')
async def main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(
        "Выберите опцию:",
        reply_markup=kb_main_menu()
    )


@start_router.callback_query(F.data == 'privacy_ok')
async def capture_privacy_policy_ok(call: CallbackQuery):
    await call.message.answer(
        "Надо зарегистрироваться:",
        reply_markup=kb_register()
    )