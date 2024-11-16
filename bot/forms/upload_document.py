from aiogram.filters import Command
from bot.create_bot import bot
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards.back_to_main_menu import kb_back_to_main_menu
from bot.utils.utils import upload_image_to_s3, generate_tmp_filename, add_data_to_key


class Form(StatesGroup):
    title = State()
    document = State()


upload_document_router = Router()


@upload_document_router.message(Command('test'))
async def start_upload_document(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Пожалуйста, назовите документ.')
    await state.set_state(Form.title)


@upload_document_router.message(F.text, Form.title)
async def capture_title(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Отправляй фото')
    await state.set_state(Form.document)


@upload_document_router.message(F.photo, Form.document)
async def capture_photo(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        name = await state.get_value('name')
        photo = message.photo[-1]

        file_info = await bot.get_file(photo.file_id)
        file_path = file_info.file_path

        tmp_file_name = generate_tmp_filename(message.from_user.id)
        await bot.download_file(file_path, tmp_file_name)

        key = add_data_to_key(name)
        upload_image_to_s3(tmp_file_name, key)
        await state.update_data(document=key)
        await message.answer(
            'Хорошо! Начинаю распознавать файл. Когда всё будет готово, я отправлю результат в чат.',
            reply_markup=kb_back_to_main_menu()
        )
