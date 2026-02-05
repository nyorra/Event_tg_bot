from aiogram import types


def get_enroll_coffee_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Ввести код", callback_data="coffee_code_input"
            )
        ],
        [types.InlineKeyboardButton(text="Назад", callback_data="back_button")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_retry_code_input_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Ввести заново", callback_data="coffee_code_input"
            )
        ],
        [types.InlineKeyboardButton(text="Назад", callback_data="back_button")],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
