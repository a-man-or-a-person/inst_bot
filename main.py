import asyncio
import logging
import os

import dotenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from insta.download import DownloadReel
from insta.post import PostReel
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

    # selection = input("Download or post")
    # if selection == "d":
    #     with open(r"C:\Users\User\Desktop\reel_download.txt", "r") as file:
    #         hrefs = file.readlines()
    #         download_bot = DownloadReel()
    #         for link in hrefs:
    #             download_bot.download_reel(link)
    # elif selection == "p":
    #     load_dotenv()
    #     post_bot = PostReel()
    #     for video in os.listdir(os.getenv("REELS_PATH")):
    #         full_vid_path = os.path.join(os.getenv("REELS_PATH"), video)
    #         post_bot.post_reel(full_vid_path)
    #         os.remove(full_vid_path)
    #         print(f"Done: {full_vid_path}")
    # else:
    #     print("Wrong selection")
