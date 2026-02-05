from typing import List

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_quiz_start_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="✏️ Пройти викторину", callback_data="Quiz")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_quiz_keyboard(
    options: List[str], question_index: int = 0
) -> InlineKeyboardMarkup:
    buttons = []
    for i, opt in enumerate(options):
        buttons.append(
            [
                InlineKeyboardButton(
                    text=opt, callback_data=f"quiz_answer:{question_index}:{i}"
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
