from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin_panel.keyboards.points import get_back_to_points_keyboard
from src.bot import messages
from src.bot.states import AdminAddPointsStates
from src.bot.utils.aiogram import save_user_message, save_messages_id
from src.database.models import User

add_points_router = Router()


@add_points_router.callback_query(F.data == "add_points")
async def add_points_start(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)

    msg = await callback.message.answer(messages.POINTS_ADD)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)

    await state.set_state(AdminAddPointsStates.waiting_for_user_id)
    await callback.answer()


@add_points_router.message(AdminAddPointsStates.waiting_for_user_id)
async def points_input_user_id(message: Message, state: FSMContext):
    await save_user_message(message, state)

    if not message.text.isdigit():
        msg = await message.answer(messages.USER_ID_ERROR)
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        return

    user_id = int(message.text.strip())
    await state.update_data(user_id=user_id)

    msg = await message.answer(messages.POINTS_ADD_AMOUNT)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)

    await state.set_state(AdminAddPointsStates.waiting_for_amount)


@add_points_router.message(AdminAddPointsStates.waiting_for_amount)
async def points_input_amount(
    message: Message, state: FSMContext, session: AsyncSession
):
    await save_user_message(message, state)

    if not message.text.isdigit():
        msg = await message.answer(messages.POINTS_AMOUNT_ERROR)
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        return

    amount = int(message.text.strip())
    state_data = await state.get_data()
    user_id = state_data.get("user_id")

    result = await session.execute(select(User).where(User.tg_id == user_id))
    user: User | None = result.scalar_one_or_none()

    if not user:
        msg = await message.answer(messages.USER_ID_ERROR)
    else:
        user.points += amount
        await session.commit()
        msg = await message.answer(
            messages.ADD_SUCCESS.format(user_id=user_id, points=amount),
            reply_markup=get_back_to_points_keyboard(),
        )

    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
