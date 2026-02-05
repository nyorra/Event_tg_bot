import asyncio
import logging

from aiogram import Dispatcher, Bot

from src.bootstrap import lifespan
from src.settings import settings

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    async with lifespan(bot, dp):
        try:
            await dp.start_polling(bot)
        except Exception as e:
            logging.exception("Ошибка при запуске бота:", exc_info=e)
        finally:
            await bot.session.close()
            from src.database.session import engine
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
