from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin_panel.keyboards.back import get_admin_back_keyboard
from src.admin_panel.utils import generate_random_code
from src.bot import messages
from src.bot.states import AdminCodeStates
from src.bot.utils.aiogram import save_user_message, save_messages_id
from src.database.models import Code

generate_codes_router = Router()


@generate_codes_router.callback_query(F.data == "generate_code")
async def ask_code_amount(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)

    msg = await callback.message.answer(messages.ADMIN_CODE_ASK_AMOUNT)
    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await state.set_state(AdminCodeStates.waiting_for_code_amount)
    await callback.answer()


@generate_codes_router.message(AdminCodeStates.waiting_for_code_amount)
async def generate_codes(message: Message, state: FSMContext, session: AsyncSession):
    await save_user_message(message, state)

    user_input = message.text.strip()
    if not user_input.isdigit() or int(user_input) < 1:
        msg = await message.answer(messages.ADMIN_CODE_INVALID_AMOUNT)
        state_data = await state.get_data()
        state_data = save_messages_id(msg.message_id, state_data)
        await state.update_data(state_data)
        return

    amount = int(user_input)
    codes = set()

    while len(codes) < amount:
        new_codes = {generate_random_code() for _ in range(amount - len(codes))}

        stmt = (
            insert(Code)
            .values(
                [{"code": code, "active": True, "used": False} for code in new_codes]
            )
            .on_conflict_do_nothing(index_elements=["code"])
            .returning(Code.code)
        )

        result = await session.execute(stmt)
        inserted_codes = [row[0] for row in result.all()]
        codes.update(inserted_codes)

    await session.commit()

    codes_text = "\n".join(codes)
    msg = await message.answer(
        messages.ADMIN_CODE_GENERATED.format(amount=amount, codes=codes_text),
        reply_markup=get_admin_back_keyboard(),
    )

    state_data = await state.get_data()
    state_data = save_messages_id(msg.message_id, state_data)
    await state.update_data(state_data)
    await state.set_state(None)
