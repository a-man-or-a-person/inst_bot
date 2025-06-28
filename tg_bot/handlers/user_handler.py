import os

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from insta.download import DownloadReel
from insta.post import PostReel

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Приветствуем вас в нашем Боте! {message.from_user.first_name}"
    )


@user_router.message(F.text.contains("http"))
async def cmd_start(message: Message):
    await message.answer(f"Link recieved\n Processing...")
    # Get link
    reel_link = message.text.split("?")[0]

    # Download reel
    download_bot = DownloadReel()
    download_bot.download_reel(reel_link)

    # Post reel
    load_dotenv()
    post_bot = PostReel()
    for video in [
        vid
        for vid in os.listdir(os.getenv("REELS_PATH"))
        if vid.lower().endswith(".mp4")
    ]:
        full_vid_path = os.path.join(os.getenv("REELS_PATH"), video)
        post_bot.post_reel(full_vid_path)
        os.remove(full_vid_path)
        print(f"Done: {full_vid_path}")

    await message.answer(f"Done")
