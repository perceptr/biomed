from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas import AnalysisSchema

KEYBOARD_SIZE = 10


def kb_list_documents(
    docs: list["AnalysisSchema"], offset: int
) -> InlineKeyboardMarkup:
    return _kb_list_documents(docs, offset, "list")


def kb_list_edit_documents(
    docs: list["AnalysisSchema"], offset: int
) -> InlineKeyboardMarkup:
    return _kb_list_documents(docs, offset, "edit")


def _kb_list_documents(
    docs: list["AnalysisSchema"], offset, action
) -> InlineKeyboardMarkup:
    next_offset = offset + KEYBOARD_SIZE
    builder = InlineKeyboardBuilder()
    for i, analysis in enumerate(docs[offset:next_offset]):
        builder.row(
            InlineKeyboardButton(
                text=f"{offset + i + 1}. {analysis.name}",
                callback_data=f"{action}_doc:{analysis.id}",
            )
        )

    if next_offset < len(docs):
        builder.row(
            InlineKeyboardButton(
                text="Следующая страница",
                callback_data=f"{action}_documents:{next_offset}",
            )
        )

    builder.row(InlineKeyboardButton(text="Отменить", callback_data="main_menu"))

    builder.adjust(1)

    return builder.as_markup()
