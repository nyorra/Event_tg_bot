from datetime import datetime, timedelta, timezone

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot import messages
from src.bot.keyboards.back import get_back_keyboard
from src.bot.keyboards.enroll_coffee import (
    get_enroll_coffee_keyboard,
    get_retry_code_input_keyboard,
)
from src.bot.states import CoffeeStates
from src.bot.utils.aiogram import save_messages_id, clear_state
from src.bot.utils.users import increment_cup, increment_points
from src.database.models import Code, User
from src.settings import settings

enroll_coffee_router = Router()


async def save_user_message(message: Message, state: FSMContext):
    state_data = await state.get_data()
    state_data = save_messages_id(message.message_id, state_data)
    await state.update_data(state_data)


@enroll_coffee_router.callback_query(F.data == "enroll_coffee")
async def enroll_coffee_handler(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)
    msg = await callback.message.answer(
        messages.ENROLL_COFFEE_MESSAGE,
        reply_markup=get_enroll_coffee_keyboard(),
        parse_mode="HTML",
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()


@enroll_coffee_router.callback_query(F.data == "coffee_code_input")
async def enroll_coffee_code_input(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)
    msg = await callback.message.answer(messages.COFFEE_INPUT)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await state.set_state(CoffeeStates.waiting_for_code)
    await callback.answer()


@enroll_coffee_router.message(CoffeeStates.waiting_for_code)
async def process_coffee_code(
    message: Message, state: FSMContext, session: AsyncSession
):
    await save_user_message(message, state)
    user_id = message.from_user.id
    user_code = message.text.strip().upper()

    now = datetime.now(timezone.utc)

    result = await session.execute(select(User).where(User.tg_id == user_id))
    user: User | None = result.scalar_one_or_none()

    if not user:
        msg = await message.answer(
            "Пользователь не найден.", reply_markup=get_back_keyboard()
        )
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        return

    if user.ban_until and user.ban_until > now:
        msg = await message.answer(
            messages.COFFEE_BANNED, reply_markup=get_back_keyboard()
        )
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        await clear_state(message.bot, user_id, state)
        return

    result = await session.execute(
        select(Code).where(
            and_(Code.code == user_code, Code.active == True, Code.used == False)
        )
    )
    code_obj = result.scalar_one_or_none()

    if code_obj:
        code_obj.used = True
        user.coffee_attempts = 0
        await session.commit()

        await increment_cup(session, user_id)
        await increment_points(session, user_id)

        msg = await message.answer(
            messages.COFFEE_SUCCESS_MESSAGE.format(cup=user.cup, points=user.points),
            reply_markup=get_back_keyboard(),
        )
    else:
        user.coffee_attempts = (user.coffee_attempts or 0) + 1

        if user.coffee_attempts >= settings.MAX_ATTEMPTS:
            user.ban_until = now + timedelta(days=1)
            user.coffee_attempts = 0
            msg = await message.answer(
                messages.COFFEE_BAN_MESSAGE, reply_markup=get_back_keyboard()
            )
        else:
            attempts_left = settings.MAX_ATTEMPTS - user.coffee_attempts
            msg = await message.answer(
                f"{messages.COFFEE_ERROR_MESSAGE}\nОсталось попыток: {attempts_left}",
                reply_markup=get_retry_code_input_keyboard(),
            )

        await session.commit()

    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
