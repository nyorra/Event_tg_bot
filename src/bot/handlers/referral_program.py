from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.bot import messages
from src.bot.keyboards.back import get_back_keyboard
from src.bot.utils.aiogram import save_messages_id, clear_state, save_user_message

referral_program_router = Router()


@referral_program_router.callback_query(F.data == "referral_program")
async def show_referral_program_handler(callback: CallbackQuery, state):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(
        messages.REFERRAL_PROGRAM_CONDITIONS,
        reply_markup=get_back_keyboard(),
        parse_mode="HTML",
    )

    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()
