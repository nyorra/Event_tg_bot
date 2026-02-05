from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot import messages
from src.bot.keyboards.back import get_back_keyboard
from src.bot.utils.aiogram import save_messages_id, clear_state
from src.database.models import User

user_points_router = Router()


async def save_user_message(message, state):
    state_data = await state.get_data()
    state_data = save_messages_id(message.message_id, state_data)
    await state.update_data(state_data)


@user_points_router.callback_query(F.data == "user_points")
async def show_user_points_handler(
    callback: CallbackQuery, state, session: AsyncSession
):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    user_id = callback.from_user.id

    result = await session.execute(select(User.points).where(User.tg_id == user_id))
    user_points = result.scalar_one_or_none() or 0

    if user_points == 0:
        text = messages.USER_POINTS_ZERO.format(points=user_points)
    else:
        text = messages.USER_POINTS.format(points=user_points)

    msg = await callback.message.answer(
        text, reply_markup=get_back_keyboard(), parse_mode="HTML"
    )

    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()
