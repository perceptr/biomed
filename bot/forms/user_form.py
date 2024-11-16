from bot.answer_texts import START_ANSWER_TEXT
from bot.create_bot import bot
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.state import State, StatesGroup
import re

from bot.filters.has_read_privacy_policy import HasReadPrivacyPolicy
from bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from bot.keyboards.main_menu import kb_main_menu
from bot.keyboards.kb_sex import kb_sex
from datetime import datetime

from bot.keyboards.privacy_policy_kb import kb_privacy_policy


def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None


class Form(StatesGroup):
    name = State()
    sex = State()
    year_of_birth = State()
    city = State()


user_info_router = Router()


@user_info_router.callback_query((F.data == 'register_user'), ~HasReadPrivacyPolicy())
async def has_not_read_privacy_policy(message: Message):
    await message.answer(
        START_ANSWER_TEXT,
        reply_markup=kb_privacy_policy()
    )


@user_info_router.callback_query((F.data == 'register_user') | (F.data == 'edit_user'), HasReadPrivacyPolicy())
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await call.message.answer('Введите имя:')
    await state.set_state(Form.name)


@user_info_router.message(F.text, Form.name)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer(
            'Введите пол:',
            reply_markup=kb_sex()
        )
    await state.set_state(Form.sex)


@user_info_router.callback_query(F.data, Form.sex)
async def capture_sex(call: CallbackQuery, state: FSMContext):
    await call.answer()
    sex = call.data.replace('uf_', '')
    await state.update_data(sex=sex)
    await call.message.answer('Введите ваш год рождения:')
    await state.set_state(Form.year_of_birth)


@user_info_router.message(F.text, Form.year_of_birth)
async def capture_year_of_birth(message: Message, state: FSMContext):
    check_year_of_birth = extract_number(message.text)

    if not check_year_of_birth or not (1900 <= check_year_of_birth <= datetime.now().year):
        await message.reply('Пожалуйста, введите корректный год рождения (от 1900 до текущего).')
        return
    await state.update_data(age=check_year_of_birth)

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Введите ваш город:')
    await state.set_state(Form.city)


@user_info_router.message(F.text, Form.city)
async def capture_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    # data = await state.get_data()
    # TODO: отправлять данные в базку
    await message.answer(
        "Готово! Мы готовы приступить к обработке ваших документов. ",
        reply_markup=kb_back_to_main_menu()
    )
    await state.clear()
