from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.admin_panel.keyboards.users import get_admin_users_keyboard
from src.bot import messages
from src.bot.utils.aiogram import save_user_message, clear_state, save_messages_id

users_panel_router = Router()


@users_panel_router.callback_query(F.data == "admin_users_panel")
async def admin_code_panel(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(
        messages.ADMIN_USERS_PANEL, reply_markup=get_admin_users_keyboard()
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()
