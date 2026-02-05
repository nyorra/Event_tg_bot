import logging

from aiogram import types, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

logger = logging.getLogger(__name__)


async def delete_messages(
    messages: list[types.Message | int], chat_id: int, bot: Bot
) -> None:
    if not messages:
        return

    messages_id = []
    for message in messages:
        if isinstance(message, types.Message):
            messages_id.append(message.message_id)
        else:
            messages_id.append(message)

    try:
        if len(messages_id) == 1:
            await bot.delete_message(chat_id, messages_id[0])
        else:
            await bot.delete_messages(chat_id, messages_id)
    except TelegramBadRequest as e:
        logging.warning(
            "Bulk delete failed for chat %s: %s. Trying individually...", chat_id, e
        )
        for m in messages_id:
            try:
                await bot.delete_message(chat_id, m)
            except TelegramBadRequest as e2:
                logging.warning(
                    "Failed to delete message %s in chat %s: %s",
                    m,
                    chat_id,
                    e2,
                )


async def clear_state(
    bot: Bot,
    chat_id: int,
    state: FSMContext,
    state_data: dict = None,
) -> None:
    if state_data is None:
        state_data = await state.get_data()

    messages_id = state_data.get("messages_id")
    if isinstance(messages_id, int):
        messages_id = [messages_id]

    await delete_messages(messages_id, chat_id, bot)
    await state.clear()
    await state.update_data(messages_id=[])
    logger.debug("Messages deleted: %s", str(messages_id))


def save_messages_id(messages_id: int | list[int], state_data: dict) -> dict:
    state_messages_id = state_data.get("messages_id", [])
    if isinstance(messages_id, list):
        for m in messages_id:
            state_messages_id.append(m)
    else:
        state_messages_id.append(messages_id)
    state_data["messages_id"] = state_messages_id
    return state_data


async def save_user_message(message: Message, state: FSMContext):
    state_data = await state.get_data()
    state_data = save_messages_id(message.message_id, state_data)
    await state.update_data(state_data)
