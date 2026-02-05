from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

# ------------------- Admin Routers -------------------
from src.admin_panel.handlers.back import admin_back_button_router
from src.admin_panel.handlers.codes.code_panel import code_panel_router
from src.admin_panel.handlers.codes.deactivate import delete_code_router
from src.admin_panel.handlers.codes.generate import generate_codes_router
from src.admin_panel.handlers.users.account.ban_user import ban_users_router
from src.admin_panel.handlers.users.account.unban_user import unban_users_router
from src.admin_panel.handlers.users.media.screenshots import screenshot_router
from src.admin_panel.handlers.users.points.add import add_points_router
from src.admin_panel.handlers.users.points.manager import points_manager_router
from src.admin_panel.handlers.users.points.remove import remove_points_router
from src.admin_panel.handlers.users.points.set import set_points_router
from src.admin_panel.handlers.users.users_panel import users_panel_router
from src.bot.handlers.ambassador_program import ambassador_program_router

# ------------------- User Routers -------------------
from src.bot.handlers.auth import auth_router
from src.bot.handlers.back import back_button_router
from src.bot.handlers.coffee.enroll_coffee import enroll_coffee_router
from src.bot.handlers.current_week.current_week import currents_week_router
from src.bot.handlers.default_mes import default_router
from src.bot.handlers.points.user_points import user_points_router
from src.bot.handlers.quests.weekly_quest import weekly_quest_router
from src.bot.handlers.quiz.quiz import quiz_router
from src.bot.handlers.referral_program import referral_program_router
from src.database.db import test_connection
from src.database.middleware import DatabaseMiddleware

# ------------------- Database -------------------
from src.database.session import async_session_maker, engine


@asynccontextmanager
async def lifespan(bot: Bot, dp: Dispatcher):
    await test_connection()

    dp.update.middleware(DatabaseMiddleware(async_session_maker))

    # --- Routers ---
    dp.include_routers(
        generate_codes_router,
        delete_code_router,
        code_panel_router,
        users_panel_router,
        ban_users_router,
        unban_users_router,
        admin_back_button_router,
        add_points_router,
        remove_points_router,
        set_points_router,
        points_manager_router,
    )

    dp.include_routers(
        auth_router,
        enroll_coffee_router,
        weekly_quest_router,
        user_points_router,
        currents_week_router,
        quiz_router,
        ambassador_program_router,
        referral_program_router,
        back_button_router,
        screenshot_router,
    )

    dp.include_routers(default_router)

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Начать заново / Главное меню"),
        ],
        BotCommandScopeDefault(),
    )

    yield

    await engine.dispose()
