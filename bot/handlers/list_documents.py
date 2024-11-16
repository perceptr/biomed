from pyexpat.errors import messages

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender
from bot.create_bot import bot
from bot.keyboards.all_kb import main_kb
from bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from bot.keyboards.list_documents_kb import kb_list_documents
from mocks.documents import get_mock_documents

list_documents_router = Router()


@list_documents_router.callback_query(F.data.startswith('list_documents'))
async def list_documents_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    offset = int(call.data.split(':')[-1])
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        docs = get_mock_documents()
        await call.message.answer(
            'Выберите интересующую вас расшифровку:',
            reply_markup=kb_list_documents(docs, offset)
        )


@list_documents_router.callback_query(F.data.startswith('list_doc_'))
async def get_current_document(call: CallbackQuery):
    await call.answer()
    qst_id = int(call.data.replace('list_doc:', ''))
    # TODO: ходим в базку за расшифровкой
    await call.message.answer(
        f"Информация по выбранному анализу: текст расшифровки документа номер {qst_id}",
        reply_markup=kb_back_to_main_menu()
    )