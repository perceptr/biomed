from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def kb_main_menu():
    keyboard_list = [
        [
            InlineKeyboardButton(
                text="Загрузить документы", callback_data="upload_documents"
            )
        ],
        [
            InlineKeyboardButton(
                text="Список расшифровок", callback_data="list_documents:0"
            )
        ],
        [InlineKeyboardButton(text="Редактировать расшифровки", callback_data="edit_documents:0")],
    ]

    return InlineKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, inline_keyboard=keyboard_list
    )
