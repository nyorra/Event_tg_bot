from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.admin_panel.handlers.codes.generate import generate_codes_router
from src.admin_panel.keyboards.main import get_admin_keyboard
from src.bot import messages
from src.bot.utils.aiogram import clear_state, save_messages_id

admin_back_button_router = Router()


@generate_codes_router.callback_query(F.data == "admin_back")
async def back_to_admin_menu(callback: CallbackQuery, state: FSMContext):
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(
        messages.ADMIN_MAIN, reply_markup=get_admin_keyboard()
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()
