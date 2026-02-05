from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin_panel.admin import is_admin
from src.admin_panel.keyboards.main import get_admin_keyboard
from src.bot.keyboards.main import get_main_keyboard
from src.bot.keyboards.privacy import get_accept_keyboard
from src.bot.keyboards.registration import (
    get_registration_keyboard,
    get_after_registration_keyboard,
    get_bad_registrtion_keyboard,
)
from src.bot.utils.aiogram import clear_state, save_messages_id, save_user_message
from src.bot.utils.data_validators import (
    validate_name,
    validate_and_format_russian_phone,
)
from src.bot.utils.users import is_user_exists, get_user, create_user
from .. import messages
from ..states import RegistrationStates

auth_router = Router()


@auth_router.message(Command("start"))
async def start_command(message: Message, state: FSMContext, session: AsyncSession):
    await save_user_message(message, state)
    await clear_state(message.bot, message.from_user.id, state)
    user_id = message.from_user.id

    if await is_admin(user_id, session):
        print("Check admin for:", user_id)
        msg = await message.answer(
            messages.ADMIN_MAIN, reply_markup=get_admin_keyboard()
        )
        state_data = save_messages_id(msg.message_id, await state.get_data())
        await state.update_data(state_data)
        return

    if await is_user_exists(session, user_id):
        user = await get_user(session, user_id)
        msg = await message.answer(
            messages.START_REGISTERED.format(username=user["username"]),
            reply_markup=get_main_keyboard(),
        )
    else:
        msg = await message.answer(
            messages.START_UNREGISTERED, reply_markup=get_accept_keyboard()
        )

    state_data = save_messages_id(msg.message_id, await state.get_data())
    await state.update_data(state_data)


@auth_router.callback_query(F.data == "privacy_accept")
async def after_privacy(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    await state.update_data(user_id=callback.from_user.id)

    msg = await callback.message.answer(messages.AFTER_PRIVACY)
    state_data = save_messages_id(msg.message_id, await state.get_data())
    await state.update_data(state_data)
    await state.set_state(RegistrationStates.waiting_for_username)
    await callback.answer()


@auth_router.message(RegistrationStates.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    await save_user_message(message, state)

    username = message.text.strip()
    if not validate_name(username):
        msg = await message.answer(messages.NAME_VALIDATION_ERROR)
    else:
        await state.update_data(username=username)
        msg = await message.answer(messages.ENTER_PHONE)
        await state.set_state(RegistrationStates.waiting_for_phone)

    state_data = save_messages_id(msg.message_id, await state.get_data())
    await state.update_data(state_data)


@auth_router.message(RegistrationStates.waiting_for_phone)
async def registration_end(message: Message, state: FSMContext):
    await save_user_message(message, state)

    phone = message.text.strip()
    is_valid, formatted_phone = validate_and_format_russian_phone(phone)

    if not is_valid:
        msg = await message.answer(messages.PHONE_VALIDATION_ERROR)
    else:
        await state.update_data(phone=formatted_phone)
        user_data = await state.get_data()
        username = user_data.get("username")
        msg = await message.answer(
            messages.CONFIRM_DATA.format(username=username, phone=formatted_phone),
            reply_markup=get_registration_keyboard(),
        )

    state_data = save_messages_id(msg.message_id, await state.get_data())
    await state.update_data(state_data)


@auth_router.callback_query(F.data == "userdata_ok")
async def userdata_is_ok(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    await save_user_message(callback.message, state)

    user_data = await state.get_data()
    username = user_data.get("username")
    phone = user_data.get("phone")
    user_id = callback.from_user.id

    await create_user(session, username, phone, user_id)

    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(
        messages.REGISTRATION_COMPLETE.format(username=username),
        reply_markup=get_after_registration_keyboard(),
    )

    state_data = save_messages_id(msg.message_id, await state.get_data())
    await state.update_data(state_data)
    await state.clear()
    await callback.answer()


@auth_router.callback_query(F.data == "userdata_not_ok")
async def userdata_is_not_ok(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(
        messages.REGISTRATION_RESTART, reply_markup=get_bad_registrtion_keyboard()
    )
    state_data = save_messages_id(msg.message_id, await state.get_data())
    await state.update_data(state_data)
    await state.clear()
    await callback.answer()


@auth_router.callback_query(F.data == "registration_again")
async def get_registration_again(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    await state.update_data(user_id=callback.from_user.id)

    msg = await callback.message.answer(messages.AFTER_PRIVACY)
    state_data = save_messages_id(msg.message_id, await state.get_data())
    await state.update_data(state_data)
    await state.set_state(RegistrationStates.waiting_for_username)
    await callback.answer()


@auth_router.callback_query(F.data == "to_main_menu")
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await save_user_message(callback.message, state)
    await clear_state(callback.bot, callback.from_user.id, state)

    msg = await callback.message.answer(
        messages.MAIN_MENU, reply_markup=get_main_keyboard()
    )
    state_data = save_messages_id(msg.message_id, await state.get_data())
    await state.update_data(state_data)
    await callback.answer()
