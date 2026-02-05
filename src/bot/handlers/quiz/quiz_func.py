from datetime import datetime, timezone, timedelta

from src.bot.keyboards.quiz import get_quiz_start_keyboard

MSK = timezone(timedelta(hours=3))
quiz_completion = {}


def is_quiz_available() -> bool:
    now = datetime.now(MSK)
    weekday = now.weekday()
    return weekday in (4, 5, 6)


def get_current_week() -> int:
    return datetime.now(MSK).isocalendar()[1]


def has_user_completed_quiz(user_id: int, week_number: int) -> bool:
    return quiz_completion.get(user_id, {}).get(week_number, False)


def complete_quiz(user_id: int, week_number: int):
    if user_id not in quiz_completion:
        quiz_completion[user_id] = {}
    quiz_completion[user_id][week_number] = True


async def send_quiz_reminder(bot, user_ids: list, brand_name: str):
    text = (
        f"Твои +5 баллов уже заждались! 🏃💨\n"
        f"Викторина по {brand_name} уже ждёт тебя\n"
        "👀 Потратил 2 минуты = залутал баллы."
    )
    keyboard = get_quiz_start_keyboard()
    for user_id in user_ids:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)


async def send_quiz_last_chance(bot, user_ids: list):
    text = "Осталось 2 часа, чтобы пройти викторину и забрать свои +5 баллов ⏰"
    for user_id in user_ids:
        await bot.send_message(chat_id=user_id, text=text)
