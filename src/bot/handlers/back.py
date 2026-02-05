from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.bot.keyboards.main import get_main_keyboard
from src.bot.utils.aiogram import clear_state, save_user_message, save_messages_id
from .. import messages

back_button_router = Router()


@back_button_router.callback_query(F.data == "back_button")
async def back_button_handler(callback: CallbackQuery, state):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)
    msg = await callback.message.answer(
        messages.MAIN_MENU, reply_markup=get_main_keyboard()
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()
