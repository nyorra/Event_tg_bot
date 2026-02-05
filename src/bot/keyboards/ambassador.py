from aiogram import types


def get_ambassador_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Узнать подробности", callback_data="ambassador_details"
            )
        ],
        [types.InlineKeyboardButton(text="Назад", callback_data="back_button")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
