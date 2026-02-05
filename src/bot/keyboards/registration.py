from aiogram import types


def get_registration_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Да, все верно", callback_data="userdata_ok")],
        [
            types.InlineKeyboardButton(
                text="Нет, надо исправить", callback_data="userdata_not_ok"
            )
        ],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_after_registration_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="В главное меню!", callback_data="to_main_menu"
            )
        ],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_bad_registrtion_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Начать заново", callback_data="registration_again"
            )
        ],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
