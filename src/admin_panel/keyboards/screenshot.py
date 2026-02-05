from aiogram import types


def get_admin_media_keyboard(
    screenshot_id: int, user_id: int
) -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text="✅ Начислить баллы",
                callback_data=f"quest_points_add:{screenshot_id}:{user_id}",
            )
        ],
        [
            types.InlineKeyboardButton(
                text="❌ Не начислять",
                callback_data=f"quest_points_false:{screenshot_id}:{user_id}",
            )
        ],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
