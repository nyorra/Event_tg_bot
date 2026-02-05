from aiogram import types


def get_coffee_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Перейти к заданию", callback_data="go_to_coffee_quest"
            )
        ],
        [types.InlineKeyboardButton(text="Назад", callback_data="back_button")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_completed_quest_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="✅ Я выполнил(а)!", callback_data="check_completed_screenshot"
            )
        ],
        [types.InlineKeyboardButton(text="Назад", callback_data="weekly_quest")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_retry_send_screenshot_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="✅ Я понял(а)!", callback_data="check_completed_screenshot"
            )
        ],
        [types.InlineKeyboardButton(text="Нет, назад", callback_data="main_menu")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
