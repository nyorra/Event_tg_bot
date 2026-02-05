from aiogram import types


def get_admin_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Коды", callback_data="admin_code_panel")],
        [
            types.InlineKeyboardButton(
                text="Пользователи", callback_data="admin_users_panel"
            )
        ],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
