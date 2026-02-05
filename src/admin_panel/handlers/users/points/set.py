from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin_panel.keyboards.points import get_back_to_points_keyboard
from src.bot import messages
from src.bot.states import AdminSetPointsStates
from src.bot.utils.aiogram import save_user_message, save_messages_id
from src.bot.utils.users import set_user_points

set_points_router = Router()


@set_points_router.callback_query(F.data == "set_points")
async def set_points_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await save_user_message(callback.message, state)

    msg = await callback.message.answer(messages.POINTS_SET)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)

    await state.set_state(AdminSetPointsStates.waiting_for_user_id)
    await callback.answer()


@set_points_router.message(AdminSetPointsStates.waiting_for_user_id)
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

    msg = await message.answer(messages.POINTS_SET_AMOUNT)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)

    await state.set_state(AdminSetPointsStates.waiting_for_amount_set)


@set_points_router.message(AdminSetPointsStates.waiting_for_amount_set)
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

    await set_user_points(session, user_id, amount)

    msg = await message.answer(
        messages.SET_SUCCESS.format(user_id=user_id, points=amount),
        reply_markup=get_back_to_points_keyboard(),
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
