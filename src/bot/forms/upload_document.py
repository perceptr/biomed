from aiogram.filters import Command
from src.bot.create_bot import bot
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.state import State, StatesGroup

from src.bot.db.db_handlers import send_analysis
from src.bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from src.bot.utils import upload_image_to_s3, generate_tmp_filename, add_data_to_key


class Form(StatesGroup):
    title = State()
    document = State()


upload_document_router = Router()


@upload_document_router.message(Command("test"))
async def start_upload_document(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer("Пожалуйста, назовите документ.")
    await state.set_state(Form.title)


@upload_document_router.callback_query(F.data == "upload_documents")
async def start_upload_document(call: CallbackQuery, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await call.message.answer("Пожалуйста, назовите документ.")
    await state.set_state(Form.title)


@upload_document_router.message(F.text, Form.title)
async def capture_title(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отправьте фото или файл форматов PDF/PNG/JPEG")
    await state.set_state(Form.document)


@upload_document_router.message(F.photo, Form.document)
async def capture_photo(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        name = await state.get_value("name")
        photo = message.photo[-1]

        file_info = await bot.get_file(photo.file_id)
        file_path = file_info.file_path

        tmp_file_name = generate_tmp_filename(message.from_user.id)
        await bot.download_file(file_path, tmp_file_name)

        key = add_data_to_key(name)
        await upload_image_to_s3(tmp_file_name, key)
        data = await state.update_data(s3_address=key)

        await send_analysis(message.from_user.id, **data)

        await message.answer(
            "Хорошо! Начинаем распознавать документ. Когда всё будет готово, мы отправим результат в чат.",
            reply_markup=kb_back_to_main_menu(),
        )


@upload_document_router.message(F.document, Form.document)
async def capture_photo(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        name = await state.get_value("name")
        photo = message.document
        file_name = photo.file_name.lower()

        if not file_name.endswith(('jpeg', 'img', 'pdf')):
            await message.answer("Возможно отправить только файлы форматов PDF/IMG/JPEG")
            return

        file_info = await bot.get_file(photo.file_id)
        file_path = file_info.file_path

        tmp_file_name = generate_tmp_filename(message.from_user.id)
        await bot.download_file(file_path, tmp_file_name)

        key = add_data_to_key(name)
        await upload_image_to_s3(tmp_file_name, key)
        data = await state.update_data(s3_address=key)

        await send_analysis(message.from_user.id, **data)

        await message.answer(
            "Хорошо! Начинаем распознавать документ. Когда всё будет готово, мы отправим результат в чат.",
            reply_markup=kb_back_to_main_menu(),
        )
        await state.clear()
