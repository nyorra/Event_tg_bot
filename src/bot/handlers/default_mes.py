from aiogram import Router, F, types
from aiogram.types import CallbackQuery

from src.admin_panel.admin import is_admin
from src.bot import messages
from src.bot.handlers.quiz.quiz_func import is_quiz_available
from src.bot.keyboards.quiz import get_quiz_start_keyboard
from src.bot.keyboards.unknown import get_ok_keyboard

default_router = Router()


@default_router.message(F.text)
async def unknown_message_handler(message: types.Message):
    text = message.text.strip().lower()
    user_id = message.from_user.id

    if not await is_admin(user_id):
        if text in ("викторина", "пройти викторину", "когда викторина"):
            if is_quiz_available():
                await message.answer(
                    "Викторина уже тут!\nЖми на кнопку «✏️ Викторина» в меню — и вперёд, за баллами!",
                    reply_markup=get_quiz_start_keyboard(),
                )
            else:
                await message.answer(
                    "Викторина: в режиме «скоро будет»\n⌛ Ждём пятницы, как кофе утра!"
                )
            return

    await message.answer(messages.INVALID_MESSAGE, reply_markup=get_ok_keyboard())


@default_router.callback_query(F.data == "ok")
async def delete_invalid_message(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
