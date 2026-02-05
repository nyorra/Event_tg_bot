from aiogram import types


def get_admin_users_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Заблокировать пользователя", callback_data="ban_user"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Разблокировать пользователя", callback_data="unban_user"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Просмотр медиа", callback_data="media_check"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Менеджер баллов", callback_data="points_manager"
            )
        ],
        [types.InlineKeyboardButton(text="Назад", callback_data="admin_back")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_users_back_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Назад", callback_data="admin_users_panel")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
