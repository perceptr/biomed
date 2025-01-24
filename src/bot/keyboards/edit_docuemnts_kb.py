from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_edit_document(doc_id: int) -> InlineKeyboardMarkup:
    keyboard_list = [
        [
            InlineKeyboardButton(
                text="Изменить название", callback_data=f"edit_doc_title:{doc_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Исправить ошибку в расшифровке",
                callback_data=f"edit_doc_text:{doc_id}",
            )
        ],
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete_doc:{doc_id}")],
        [InlineKeyboardButton(text="Отмена", callback_data=f"main_menu")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard_list)
