from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_register():
    return InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        inline_keyboard = [[InlineKeyboardButton(text="Зарегистрироваться", callback_data="register_user")]]
    )