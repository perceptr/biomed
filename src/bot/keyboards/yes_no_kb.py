from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def kb_yes_or_no() :
    keyboard_list = [
        [InlineKeyboardButton(callback_data="kb_no", text="Нет")],
        [InlineKeyboardButton(callback_data="kb_yes", text="Да")]
    ]

    return InlineKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, inline_keyboard=keyboard_list
    )