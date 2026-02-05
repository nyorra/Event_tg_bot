from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin_panel.keyboards.screenshot import get_admin_media_keyboard
from src.admin_panel.keyboards.users import get_admin_users_back_keyboard
from src.bot import messages
from src.bot.utils.aiogram import save_user_message, clear_state, save_messages_id
from src.database.models import Screenshot, User

screenshot_router = Router()


@screenshot_router.callback_query(F.data == "media_check")
async def admin_check_screenshots(
        callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    result = await session.execute(
        select(Screenshot)
        .where(Screenshot.status == "pending")
        .order_by(Screenshot.created_at)
        .limit(1)
    )
    screenshot: Screenshot | None = result.scalar_one_or_none()

    if not screenshot:
        msg = await callback.message.answer(
            messages.NO_SCREENSHOTS,
            reply_markup=get_admin_users_back_keyboard()
        )
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        await callback.answer()
        return

    msg = await callback.message.answer_photo(
        screenshot.file_id,
        caption=messages.SCREENSHOT_CAPTION.format(
            user_id=screenshot.user_id,
            screenshot_id=screenshot.id
        ),
        reply_markup=get_admin_media_keyboard(screenshot.id, screenshot.user_id),
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()


async def process_screenshot(
        callback: CallbackQuery, state: FSMContext, session: AsyncSession, approved: bool
):

    """"Универсальная функция для approve/reject скриншота.
    approved=True -> одобрить и начислить баллы
    approved=False -> отклонить без начисления баллов"""""


    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    _, screenshot_id, user_id = callback.data.split(":")
    screenshot_id, user_id = int(screenshot_id), int(user_id)

    status_value = "approved" if approved else "rejected"

    result = await session.execute(
        update(Screenshot)
        .where(and_(Screenshot.id == screenshot_id, Screenshot.status == "pending"))
        .values(
            status=status_value,
            checked_by=callback.from_user.id,
            checked_at=datetime.now(timezone.utc),
        )
    )

    if result.rowcount == 0:
        await callback.answer(
            "Скриншот уже обработан другим администратором.", show_alert=True
        )
        return

    if approved:
        await session.execute(
            update(User)
            .where(User.tg_id == user_id)
            .values(points=User.points + 3)
        )

    await session.commit()

    user_msg = (
        messages.SCREENSHOT_APPROVED_USER if approved else messages.SCREENSHOT_REJECTED_USER
    )
    msg = await callback.bot.send_message(user_id, user_msg)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)

    admin_msg = (
        messages.SCREENSHOT_APPROVED_ADMIN if approved else messages.SCREENSHOT_REJECTED_ADMIN
    )
    await callback.message.edit_caption(admin_msg)
    await callback.answer()


@screenshot_router.callback_query(F.data.startswith("quest_points_add:"))
async def approve_screenshot_handler(
        callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    await process_screenshot(callback, state, session, approved=True)


@screenshot_router.callback_query(F.data.startswith("quest_points_false:"))
async def reject_screenshot_handler(
        callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    await process_screenshot(callback, state, session, approved=False)
