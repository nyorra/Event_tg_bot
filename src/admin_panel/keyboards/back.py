from aiogram import types


def get_admin_back_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Назад", callback_data="admin_back")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
