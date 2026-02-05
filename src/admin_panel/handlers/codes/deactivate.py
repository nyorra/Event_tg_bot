from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin_panel.keyboards.back import get_admin_back_keyboard
from src.bot import messages
from src.bot.states import AdminCodeStates
from src.bot.utils.aiogram import save_user_message, clear_state, save_messages_id
from src.database.models import Code

delete_code_router = Router()


@delete_code_router.callback_query(F.data == "delete_code")
async def delete_code_start(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)

    msg = await callback.message.answer(messages.DELETE_CODE)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await state.set_state(AdminCodeStates.waiting_for_delete_code)
    await callback.answer()


@delete_code_router.message(AdminCodeStates.waiting_for_delete_code)
async def deactivate_code_input(
    message: Message, state: FSMContext, session: AsyncSession
):
    await save_user_message(message, state)

    code_to_deactivate = message.text.strip().upper()

    result = await session.execute(
        select(Code).where(Code.code == code_to_deactivate, Code.active == True)  # type: ignore
    )
    code_obj: Code | None = result.scalar_one_or_none()

    if not code_obj:
        msg_text = f"Код {code_to_deactivate} не найден или уже деактивирован."
    else:
        code_obj.active = False
        await session.commit()
        msg_text = f"Код {code_to_deactivate} успешно деактивирован."

    msg = await message.answer(msg_text, reply_markup=get_admin_back_keyboard())
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await state.set_state(None)


@delete_code_router.callback_query(F.data == "admin_back")
async def back_to_admin_menu(callback: CallbackQuery, state: FSMContext):
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(
        messages.MAIN_MENU, reply_markup=get_admin_back_keyboard()
    )
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await callback.answer()
