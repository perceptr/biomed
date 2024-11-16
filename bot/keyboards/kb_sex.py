from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def kb_sex():
    kb_list = [
        [
            InlineKeyboardButton(text="Мужской 🙎‍♂️", callback_data='uf_M'),
            InlineKeyboardButton(text="Женский 🙍‍♀️", callback_data='uf_F')
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Выберите пол:'
    )

    return keyboard
