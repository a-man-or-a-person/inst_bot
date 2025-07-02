import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from tg_bot.handlers.user_handler import user_router


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_API"))

    dp = Dispatcher()

    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
