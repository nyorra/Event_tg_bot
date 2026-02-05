from aiogram import types


def get_admin_code_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Сгенерировать код", callback_data="generate_code"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Деактивировать код", callback_data="delete_code"
            )
        ],
        [types.InlineKeyboardButton(text="Назад", callback_data="admin_back")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
