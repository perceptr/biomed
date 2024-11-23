from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_back_to_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')]
        ]
    )