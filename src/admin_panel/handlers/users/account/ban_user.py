from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin_panel.keyboards.users import get_admin_users_back_keyboard
from src.bot import messages
from src.bot.states import AdminBanStates
from src.bot.utils.aiogram import save_user_message, clear_state, save_messages_id
from src.database.models import User

ban_users_router = Router()


@ban_users_router.callback_query(F.data == "ban_user")
async def ban_user_start(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(messages.BAN_ENTER_USER_ID)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await state.set_state(AdminBanStates.waiting_for_user_id)
    await callback.answer()


@ban_users_router.message(AdminBanStates.waiting_for_user_id)
async def ban_user_input_id(message: Message, state: FSMContext, session: AsyncSession):
    await save_user_message(message, state)

    if not message.text.isdigit():
        msg = await message.answer(messages.BAN_USER_ID_ERROR)
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        return

    user_id = int(message.text.strip())

    await session.execute(update(User).where(User.tg_id == user_id).values())
    user_exists = await session.get(User, user_id)
    if not user_exists:
        msg = await message.answer(
            messages.USER_NOT_EXIST, reply_markup=get_admin_users_back_keyboard()
        )
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        return

    await state.update_data(user_id=user_id)

    msg = await message.answer(messages.BAN_ENTER_DATE)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await state.set_state(AdminBanStates.waiting_for_ban_date)


@ban_users_router.message(AdminBanStates.waiting_for_ban_date)
async def ban_user_input_date(
    message: Message, state: FSMContext, session: AsyncSession
):
    await save_user_message(message, state)

    date_text = message.text.strip()
    try:
        ban_until = datetime.strptime(date_text, "%Y-%m-%d")
        ban_until = ban_until.replace(
            hour=23, minute=59, second=59, tzinfo=timezone.utc
        )
    except ValueError:
        msg = await message.answer(messages.BAN_DATE_ERROR)
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        return

    state_data = await state.get_data()
    user_id = state_data.get("user_id")

    await session.execute(
        update(User).where(User.tg_id == user_id).values(ban_until=ban_until)
    )
    await session.commit()

    msg = await message.answer(
        messages.BAN_SUCCESS.format(user_id=user_id, ban_until=ban_until.date()),
        reply_markup=get_admin_users_back_keyboard(),
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
