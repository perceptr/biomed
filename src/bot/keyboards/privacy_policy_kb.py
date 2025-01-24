from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def kb_privacy_policy():
    kb_list = [
        [InlineKeyboardButton(text="Политика конфиденциальности", url="https://www.consultant.ru/document/cons_doc_LAW_61801/")],
        [
            InlineKeyboardButton(
                text="Я ознакомился и согласен", callback_data="privacy_ok"
            )
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list,
        resize_keyboard=True,
    )

    return keyboard
