from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.bot import messages
from src.bot.keyboards.ambassador import get_ambassador_keyboard
from src.bot.keyboards.back import get_back_keyboard
from src.bot.utils.aiogram import save_messages_id, clear_state, save_user_message

ambassador_program_router = Router()


@ambassador_program_router.callback_query(F.data == "ambassador_program")
async def show_ambassador_program_handler(callback: CallbackQuery, state):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(
        messages.AMBASSADOR_PROGRAM_INFO,
        reply_markup=get_ambassador_keyboard(),
        parse_mode="HTML",
    )

    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()


@ambassador_program_router.callback_query(F.data == "ambassador_details")
async def show_ambassador_details_handler(callback: CallbackQuery, state):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(
        messages.AMBASSADOR_DETAIL_INFO,
        reply_markup=get_back_keyboard(),
        parse_mode="HTML",
    )

    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()
