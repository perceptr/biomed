from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def kb_apply_file_for_work() :
    keyboard_list = [
        [InlineKeyboardButton(callback_data="get_file", text="Получить документ для расшифровки")]
    ]

    return InlineKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, inline_keyboard=keyboard_list
    )