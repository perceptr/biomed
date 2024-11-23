from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from src.bot.create_bot import bot
from src.bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from src.bot.keyboards.edit_docuemnts_kb import kb_edit_document
from src.bot.keyboards.list_documents_kb import kb_list_edit_documents
from src.bot.keyboards.main_menu import kb_main_menu
from mocks.documents import get_mock_documents

edit_documents_router = Router()


class EditDocument(StatesGroup):
    title = State()
    text = State()
    are_you_sure = State()


@edit_documents_router.callback_query(F.data.startswith("edit_documents"))
async def handle_list_edit_documents(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    offset = int(call.data.split(":")[-1])
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        docs = get_mock_documents()
        await call.message.answer(
            "Выберите интересующую вас расшифровку:",
            reply_markup=kb_list_edit_documents(docs, offset),
        )


@edit_documents_router.message(Command("test2"))
async def handle_list_edit_documents(message: Message, state: FSMContext):
    await state.clear()
    offset = 0
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        docs = get_mock_documents()
        await message.answer(
            "Выберите интересующую вас расшифровку:",
            reply_markup=kb_list_edit_documents(docs, offset),
        )


@edit_documents_router.callback_query(F.data.startswith("edit_doc_title"))
async def handle_edit_doc_title(call: CallbackQuery, state: FSMContext):
    await call.answer()
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await call.message.answer("Введите новое название расшифровки:")
    await state.set_state(EditDocument.title)


@edit_documents_router.callback_query(F.data.startswith("edit_doc:"))
async def handle_single_edit_document(call: CallbackQuery, state: FSMContext):
    await call.answer()
    doc_id = int(call.data.split(":")[-1])
    await state.update_data(doc_id=doc_id)
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        # TODO: ходим в базку за расшифровкой
        text = "test"
        await state.update_data(title="title", text=text)
        await call.message.answer(
            f"Информация по выбранному анализу: "
            f"текст расшифровки {doc_id}\n"
            f"Что вы хотите сделать с анализом?",
            reply_markup=kb_edit_document(doc_id),
        )


@edit_documents_router.message(F.text, EditDocument.title)
async def capture_title(message: Message, state: FSMContext):
    # TODO: ходим в базку, всё из этого меняем
    await state.clear()
    await message.answer(
        f'Название изменено на: "{message.text}"', reply_markup=kb_back_to_main_menu()
    )


@edit_documents_router.callback_query(F.data.startswith("edit_doc_text"))
async def handle_edit_doc_text(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        "Пожалуйста, укажите, что именно нужно исправить в расшифровке."
    )
    await state.set_state(EditDocument.text)


@edit_documents_router.message(F.text, EditDocument.text)
async def capture_title(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Спасибо за уточнение. Ваш запрос на доработку отправлен оператору. "
        "Мы уведомим вас, когда исправленная расшифровка будет готова.",
        reply_markup=kb_back_to_main_menu(),
    )


@edit_documents_router.callback_query(F.data.startswith("delete_doc"))
async def handle_delete_doc(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        'Вы действительно хотите удалить расшифровку анализа? Напишите "Удалить"'
    )
    await state.set_state(EditDocument.are_you_sure)


@edit_documents_router.message(F.text == "Удалить", EditDocument.are_you_sure)
async def yes_i_am_sure(message: Message, state: FSMContext):
    await state.clear()
    # TODO: удаляем
    title = await state.get_value("title")  # не видим номер расшифровки пока что
    await message.answer(
        f"Расшифровка под номером № {title} удалена",
        reply_markup=kb_back_to_main_menu(),
    )


@edit_documents_router.message(F.text, EditDocument.are_you_sure)
async def no_i_am_not_sure(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Расшифровка не удалена.", reply_markup=kb_main_menu())
