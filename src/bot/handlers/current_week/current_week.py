from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from src.bot import messages
from src.bot.handlers.current_week.current_week_data import get_week_info
from src.bot.keyboards.back import get_back_keyboard
from src.bot.utils.aiogram import save_messages_id, clear_state
from src.bot.utils.calc_week import calculate_current_week

currents_week_router = Router()


async def save_user_message(message, state):
    state_data = await state.get_data()
    state_data = save_messages_id(message.message_id, state_data)
    await state.update_data(state_data)


@currents_week_router.callback_query(F.data == "current_week")
async def show_current_week_handler(callback: CallbackQuery, state):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    current_week = calculate_current_week()
    if current_week <= 0:
        text = "Проект еще не начался! Старт 1.10.2025"
        msg = await callback.message.answer(text, reply_markup=get_back_keyboard())
    else:
        week_data = get_week_info(current_week)
        text = messages.CURRENT_WEEK_INFO.format(current_week=current_week, **week_data)
        photo = FSInputFile(week_data["photo"])
        msg = await callback.message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=get_back_keyboard(),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()
