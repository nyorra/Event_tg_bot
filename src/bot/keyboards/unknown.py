from aiogram import types


def get_ok_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [[types.InlineKeyboardButton(text="Ок!", callback_data="ok")]]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
