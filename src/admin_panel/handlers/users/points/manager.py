from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.admin_panel.keyboards.points import get_admin_points_keyboard
from src.bot import messages
from src.bot.states import AdminManagerPointsStates
from src.bot.utils.aiogram import save_user_message, clear_state, save_messages_id

points_manager_router = Router()


@points_manager_router.callback_query(F.data == "points_manager")
async def manager_points_start(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(
        messages.POINTS_MANAGER, reply_markup=get_admin_points_keyboard()
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await state.set_state(AdminManagerPointsStates.waiting_for_user_id)
