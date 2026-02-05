from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot import messages
from src.bot.handlers.quests.weekly_quest_data import get_weekly_data
from src.bot.keyboards.back import get_back_keyboard
from src.bot.keyboards.weekly_quest import (
    get_coffee_keyboard,
    get_completed_quest_keyboard,
    get_retry_send_screenshot_keyboard,
)
from src.bot.states import ScreenshotStates
from src.bot.utils.aiogram import save_messages_id, clear_state, save_user_message
from src.bot.utils.calc_week import calculate_current_week
from src.database.models import Screenshot

weekly_quest_router = Router()


@weekly_quest_router.callback_query(F.data == "weekly_quest")
async def weekly_quest_intro(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)
    msg = await callback.message.answer(
        messages.WEEKLY_QUEST_INTRO,
        reply_markup=get_coffee_keyboard(),
        parse_mode="HTML",
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()


@weekly_quest_router.callback_query(F.data == "go_to_coffee_quest")
async def weekly_quest_task(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)
    current_week = calculate_current_week()
    data = get_weekly_data(current_week)
    weekly_text = messages.WEEKLY_QUEST_TASK.format(**data)
    msg = await callback.message.answer(
        weekly_text, reply_markup=get_completed_quest_keyboard()
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()


@weekly_quest_router.callback_query(F.data == "check_completed_screenshot")
async def request_screenshot(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)
    msg = await callback.message.answer(messages.SEND_SCREENSHOT)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await state.set_state(ScreenshotStates.waiting_for_screenshot)
    await callback.answer()


@weekly_quest_router.message(
    ScreenshotStates.waiting_for_screenshot, F.content_type == ContentType.PHOTO
)
async def process_screenshot(
    message: Message, state: FSMContext, session: AsyncSession
):
    await save_user_message(message, state)
    photo = message.photo[-1]
    file_id = photo.file_id
    user_id = message.from_user.id

    stmt = insert(Screenshot).values(user_id=user_id, file_id=file_id, status="pending")
    await session.execute(stmt)
    await session.commit()

    msg = await message.answer(
        messages.SCREENSHOT_DONE, reply_markup=get_back_keyboard()
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)


@weekly_quest_router.message(ScreenshotStates.waiting_for_screenshot)
async def handle_wrong_content(message: Message, state: FSMContext):
    await save_user_message(message, state)
    msg = await message.answer(
        messages.NOT_SCREENSHOT, reply_markup=get_retry_send_screenshot_keyboard()
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
