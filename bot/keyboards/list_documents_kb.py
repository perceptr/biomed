import enum

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

KEYBOARD_SIZE = 10


def kb_list_documents(docs: list[tuple[int, str]], offset: int) -> InlineKeyboardMarkup:
    return _kb_list_documents(docs, offset, 'list')


def kb_list_edit_documents(docs: list[tuple[int, str]], offset: int) -> InlineKeyboardMarkup:
    return _kb_list_documents(docs, offset, 'edit')


def _kb_list_documents(docs: list[tuple[int, str]], offset, action) -> InlineKeyboardMarkup:
    next_offset = offset + KEYBOARD_SIZE
    builder = InlineKeyboardBuilder()
    for i, (doc_id, doc_title) in enumerate(docs[offset:next_offset]):
        builder.row(
            InlineKeyboardButton(text=f'{offset + i + 1}. {doc_title}', callback_data=f'{action}_doc:{doc_id}')
        )

    if next_offset < len(docs):
        builder.row(
            InlineKeyboardButton(text='Следующая страница', callback_data=f'{action}_documents:{next_offset}')
        )

    builder.adjust(1)

    return builder.as_markup()