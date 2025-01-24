from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_new_token():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Попробовать ещё раз", callback_data="try_new_token")
            ],
            [
                InlineKeyboardButton(
                    text="Вернуться в главное меню", callback_data="main_menu"
                )
            ]
        ]
    )
