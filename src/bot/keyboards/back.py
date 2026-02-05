from aiogram import types


def get_back_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [[types.InlineKeyboardButton(text="Назад", callback_data="back_button")]]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
