from aiogram import types


def get_accept_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Я ознакомлен(а) и согласен(а)", callback_data="privacy_accept"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Политика конфиденциальности",
                callback_data="privacy_policy",
                url="https://music.yandex.ru/",
            )
        ],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
