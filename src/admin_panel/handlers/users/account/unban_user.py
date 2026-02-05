from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin_panel.keyboards.back import get_admin_back_keyboard
from src.admin_panel.keyboards.users import get_admin_users_back_keyboard
from src.bot import messages
from src.bot.states import AdminUnbanStates
from src.bot.utils.aiogram import save_user_message, clear_state, save_messages_id
from src.database.models import User

unban_users_router = Router()


@unban_users_router.callback_query(F.data == "unban_user")
async def unban_user_start(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(messages.UNBAN_ENTER_USER_ID)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await state.set_state(AdminUnbanStates.waiting_for_user_id)
    await callback.answer()


@unban_users_router.message(AdminUnbanStates.waiting_for_user_id)
async def unban_user_input_id(
    message: Message, state: FSMContext, session: AsyncSession
):
    await save_user_message(message, state)

    if not message.text.isdigit():
        msg = await message.answer(messages.UNBAN_USER_ID_ERROR)
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        return

    user_id = int(message.text.strip())

    result = await session.execute(select(User).where(User.tg_id == user_id))
    user: User | None = result.scalar_one_or_none()

    if not user:
        msg = await message.answer(
            messages.USER_NOT_EXIST, reply_markup=get_admin_users_back_keyboard()
        )
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        return

    user.ban_until = None
    await session.commit()

    msg = await message.answer(
        messages.UNBAN_SUCCESS.format(user_id=user_id),
        reply_markup=get_admin_back_keyboard(),
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
