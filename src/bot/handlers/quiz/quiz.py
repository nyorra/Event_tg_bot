from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot import messages
from src.bot.handlers.quiz.quiz_data import get_weekly_quiz
from src.bot.handlers.quiz.quiz_func import quiz_completion
from src.bot.keyboards.back import get_back_keyboard
from src.bot.keyboards.quiz import get_quiz_keyboard
from src.bot.utils.aiogram import save_messages_id, save_user_message, clear_state
from src.bot.utils.users import (
    has_user_completed_quiz,
    complete_quiz,
    increment_points,
)

quiz_router = Router()
WEEK_NUMBER = 4


@quiz_router.callback_query(F.data == "Quiz")
async def start_quiz(callback: CallbackQuery, state, session: AsyncSession):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    user_id = callback.from_user.id
    questions = get_weekly_quiz(WEEK_NUMBER)

    if not questions:
        msg = await callback.message.answer(
            "🚫 Вопросы пока недоступны", reply_markup=get_back_keyboard()
        )
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        await callback.answer()
        return

    if await has_user_completed_quiz(session, user_id, WEEK_NUMBER):
        msg = await callback.message.answer(
            "👽 Чилл, баллы уже в твоём кармане!\nЗа вторым заходом — в следующую пятницу, договорились? 😉",
            reply_markup=get_back_keyboard(),
        )
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        await callback.answer()
        return

    quiz_completion[user_id] = {"correct_count": 0}
    first_question = questions[0]
    keyboard = get_quiz_keyboard(first_question["options"], question_index=0)
    msg = await callback.message.answer(
        f"❓ {first_question['question']}", reply_markup=keyboard
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()


@quiz_router.callback_query(F.data.startswith("quiz_answer:"))
async def handle_quiz_answer(callback: CallbackQuery, state, session: AsyncSession):
    await save_user_message(callback.message, state)

    user_id = callback.from_user.id
    _, q_index_str, opt_index_str = callback.data.split(":")
    question_index = int(q_index_str)
    selected_option = int(opt_index_str)

    questions = get_weekly_quiz(WEEK_NUMBER)
    if question_index >= len(questions):
        await callback.answer("❌ Вопрос не найден")
        return

    question_data = questions[question_index]
    correct_option = question_data["answer"]

    if selected_option == correct_option:
        result_text = "✅ Правильно!"
        quiz_completion[user_id]["correct_count"] += 1
    else:
        result_text = f"❌ Неправильно! Правильный ответ: {question_data['options'][correct_option]}"

    msg = await callback.message.answer(result_text)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)

    next_index = question_index + 1
    if next_index < len(questions):
        next_question = questions[next_index]
        keyboard = get_quiz_keyboard(
            next_question["options"], question_index=next_index
        )
        msg = await callback.message.answer(
            f"❓ {next_question['question']}", reply_markup=keyboard
        )
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
    else:
        if not await has_user_completed_quiz(session, user_id, WEEK_NUMBER):
            await complete_quiz(session, user_id, WEEK_NUMBER)

            correct_count = quiz_completion[user_id].get("correct_count", 0)
            if correct_count > 0:
                await increment_points(session, user_id, amount=correct_count)

            if correct_count == len(questions):
                final_text = messages.QUIZ_FULL_CORRECTE.format(points=correct_count)
            elif correct_count > 0:
                final_text = messages.QUIZ_SAME_CORRECT.format(points=correct_count)
            else:
                final_text = messages.QUIZ_ZERO_CORRECT

            msg = await callback.message.answer(
                final_text, reply_markup=get_back_keyboard()
            )
            state_data = await state.get_data()
            state_data = save_messages_id(msg.message_id, state_data)
            await state.update_data(state_data)

            quiz_completion[user_id]["correct_count"] = 0
