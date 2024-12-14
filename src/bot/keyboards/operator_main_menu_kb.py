from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def kb_operator_main_menu() :
    keyboard_list = [
        [InlineKeyboardButton(callback_data="take_on_task", text="Взять файл в работу")]
    ]

    return InlineKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, inline_keyboard=keyboard_list
    )