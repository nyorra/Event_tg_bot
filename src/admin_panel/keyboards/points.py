from aiogram import types


def get_admin_points_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Прибавить баллы", callback_data="add_points"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Отнять баллы", callback_data="remove_points"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Установить баллы", callback_data="set_points"
            )
        ],
        [types.InlineKeyboardButton(text="Назад", callback_data="admin_back")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_to_points_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Назад", callback_data="points_manager")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
