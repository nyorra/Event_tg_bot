from aiogram import types

from src.bot.handlers.quiz.quiz_func import is_quiz_available
from src.bot.utils.calc_week import calculate_current_week


def get_main_keyboard() -> types.InlineKeyboardMarkup:
    current_week = calculate_current_week()
    quiz_available = is_quiz_available()

    buttons = [
        [
            types.InlineKeyboardButton(
                text="🎯 Задание недели", callback_data="weekly_quest"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="☕️ Записать кофе", callback_data="enroll_coffee"
            )
        ],
        [types.InlineKeyboardButton(text="🏆 Мои баллы", callback_data="user_points")],
        [
            types.InlineKeyboardButton(
                text="❤️ Текущая неделя", callback_data="current_week"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="📢 Реферальная программа", callback_data="referral_program"
            )
        ],
    ]

    if current_week <= 3:
        buttons.append(
            [
                types.InlineKeyboardButton(
                    text="🌟 Амбассадорская программа",
                    callback_data="ambassador_program",
                )
            ]
        )

    if quiz_available:
        buttons.append(
            [types.InlineKeyboardButton(text="✏️ Викторина", callback_data="Quiz")]
        )

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
