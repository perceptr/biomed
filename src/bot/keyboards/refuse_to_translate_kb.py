from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def kb_refuse_to_translate() :
    keyboard_list = [
        [InlineKeyboardButton(callback_data="refuse_to_translate", text="Отказаться")]
    ]

    return InlineKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, inline_keyboard=keyboard_list
    )