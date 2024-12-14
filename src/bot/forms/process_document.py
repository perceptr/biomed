from aiogram.filters import Command
from pyexpat.errors import messages

from src.bot.create_bot import bot
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.state import State, StatesGroup

from src.bot.db.db_handlers import send_analysis, count_uncompleted_analysis, set_operator_to_analysis, \
    unset_operator_to_analysis, finish_document
from src.bot.forms.utils import get_analysis_photo
from src.bot.keyboards.apply_file_for_work_kb import kb_apply_file_for_work
from src.bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from src.bot.keyboards.refuse_to_translate_kb import kb_refuse_to_translate
from src.bot.keyboards.yes_no_kb import kb_yes_or_no
from src.bot.utils import upload_image_to_s3, generate_tmp_filename, add_data_to_key, download_image_from_s3
from src.schemas import AnalysisSchema


class Document(StatesGroup):
    document = State()
    text = State()
    verify = State()
    refuse = State()

process_document_router = Router()

@process_document_router.callback_query(F.data == "take_on_task")
async def start_process_document(call: CallbackQuery, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        docs_count = await count_uncompleted_analysis()
        if docs_count == 0:
            await call.message.answer("На данный момент нет файлов для расшифровки")
            return
        await call.message.answer(
            f"Файлов для расшфировки: {docs_count}. Вы можете начать работу.",
            reply_markup=kb_apply_file_for_work()
        )
    await state.set_state(Document.document)


@process_document_router.callback_query(F.data, Document.document)
async def capture_document(call: CallbackQuery, state: FSMContext):
    async with ChatActionSender.upload_photo(bot=bot, chat_id=call.message.chat.id):
        print(f'capture document id {call.from_user.id}')
        analysis = await set_operator_to_analysis(call.from_user.id)
        if analysis is None:
           await call.message.answer(
               "Произошла ошибка. Попробуйте ещё раз.",
               reply_markup=kb_back_to_main_menu()
           )
           await state.clear()


        await state.update_data(analysis=analysis)

        photo = await get_analysis_photo(call.message.from_user.id, analysis)

        await call.message.answer_photo(
            photo,
            caption="Переведите файл в текст по установленному формату и введите результат в чат.",
            reply_markup=kb_refuse_to_translate()
        )
        await state.set_state(Document.text)


@process_document_router.message(F.text, Document.text)
async def verify_sending(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(
        "Вы уверены, что хотите отправить введенные данные пользователю?",
        reply_markup=kb_yes_or_no()
    )
    await state.set_state(Document.verify)



async def verify_sending_yes(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите текст расшифроки:")
    await state.set_state(Document.text)


@process_document_router.callback_query(F.data == "refuse_to_translate", Document.text)
async def refuse_to_process(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        "Вы уверены, что хотите отказаться от файла?",
        reply_markup=kb_yes_or_no()
    )
    await state.set_state(Document.refuse)


process_document_router.callback_query.register(verify_sending_yes, F.data == "kb_no", Document.verify)
process_document_router.callback_query.register(verify_sending_yes, F.data == "kb_no", Document.refuse)


@process_document_router.callback_query(F.data == "kb_yes", Document.refuse)
async def refuse_to_process_yes(call: CallbackQuery, state: FSMContext):
    print(f'refuse id {call.from_user.id}')
    await unset_operator_to_analysis(call.from_user.id)
    await state.clear()
    await call.message.answer(
        "Вы отказались от файла.",
        reply_markup=kb_back_to_main_menu()
    )



@process_document_router.callback_query(F.data == "kb_yes", Document.verify)
async def apply_document(call: CallbackQuery, state: FSMContext):
    analysis: AnalysisSchema = await state.get_value('analysis')
    text = await state.get_value('text')
    await bot.send_message(analysis.user.telegram_id, f'А вот ваш текст {text}')
    await finish_document(analysis.id, text)
    await call.message.answer(
        'Расшифровка успешно добавлена',
        reply_markup=kb_back_to_main_menu()
    )
    await state.clear()



