from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from src.bot.create_bot import bot
from src.bot.db.db_handlers import get_documents_by_user, get_document
from src.bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from src.bot.keyboards.list_documents_kb import kb_list_documents
from typing import TYPE_CHECKING

from src.bot.utils.utils import get_analysis_photo

if TYPE_CHECKING:
    from src.schemas import AnalysisSchema

list_documents_router = Router()


@list_documents_router.callback_query(F.data.startswith("list_documents"))
async def list_documents_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    offset = int(call.data.split(":")[-1])
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        docs: list["AnalysisSchema"] = await get_documents_by_user(
            call.from_user.id
        )
        await call.message.answer(
            "Выберите интересующую вас расшифровку:",
            reply_markup=kb_list_documents(docs, offset),
        )


@list_documents_router.callback_query(F.data.startswith("list_doc:"))
async def get_current_document(call: CallbackQuery):
    await call.answer()
    qst_id = int(call.data.replace("list_doc:", ""))
    analysis = await get_document(qst_id)
    photo = await get_analysis_photo(analysis)
    await call.message.answer_photo(
        photo,
        caption=f"""
Информация по расшифровке "{analysis.name}":

{analysis.result}
""",
        reply_markup=kb_back_to_main_menu(),
    )
