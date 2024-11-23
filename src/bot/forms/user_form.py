from src.bot.answer_texts import START_ANSWER_TEXT
from src.bot.create_bot import bot
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.state import State, StatesGroup

from src.bot.db.db_handlers import create_user
from src.bot.filters.has_read_privacy_policy import HasReadPrivacyPolicyFilter
from src.bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from src.bot.keyboards.kb_sex import kb_sex
from src.bot.utils import extract_number

from src.bot.keyboards.privacy_policy_kb import kb_privacy_policy
from src.bot.utils.utils import get_gender_by_choice
from src.bot.validators import validate_year_of_birth


class Form(StatesGroup):
    name = State()
    sex = State()
    year_of_birth = State()
    city = State()


user_info_router = Router()


@user_info_router.callback_query((F.data == 'register_user'), ~HasReadPrivacyPolicyFilter())
async def has_not_read_privacy_policy(message: Message):
    await message.answer(
        START_ANSWER_TEXT,
        reply_markup=kb_privacy_policy()
    )


@user_info_router.callback_query((F.data == 'register_user') | (F.data == 'edit_user'), HasReadPrivacyPolicyFilter())
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
    await state.update_data(gender=get_gender_by_choice(call.data))
    await call.message.answer('Введите ваш год рождения:')
    await state.set_state(Form.year_of_birth)


@user_info_router.message(F.text, Form.year_of_birth)
async def capture_year_of_birth(message: Message, state: FSMContext):
    year_of_birth = extract_number(message.text)

    if not validate_year_of_birth(year_of_birth):
        await message.reply('Пожалуйста, введите корректный год рождения (от 1900 до текущего).')
        return
    await state.update_data(birth_year=year_of_birth)

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Введите ваш город:')
    await state.set_state(Form.city)


@user_info_router.message(F.text, Form.city)
async def capture_city(message: Message, state: FSMContext):
    data = await state.update_data(city=message.text)

    await create_user(message.from_user.id, **data)

    await message.answer(
        "Готово! Мы готовы приступить к обработке ваших документов. ",
        reply_markup=kb_back_to_main_menu()
    )
    await state.clear()
