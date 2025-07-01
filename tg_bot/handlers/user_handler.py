import os

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from insta.download import DownloadReel
from insta.post import AsyncPostReel

from DB.orm import add_link, get_links, create_tables, delete_link

user_router = Router()
post_bot = AsyncPostReel()

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
    await add_link(message.from_user.id, message.from_user.first_name, reel_link)
    await message.answer('Done')


@user_router.message(F.text.contains("Links"))
async def cmd_start(message: Message):
    await message.answer(f"Getting links...")
    await message.answer(str(await get_links()))


@user_router.message(F.text == "DB")
async def cmd_start(message: Message):
    await create_tables()
    await message.answer(f"Dropping tables")


@user_router.message(F.text == 'post')
async def cmd_start(message: Message):
    await message.answer(f"Processing...")
    # Get link
    reel_link = await get_links()
    reel_link = reel_link[0].split()
    # Delete link
    await delete_link(reel_link[0])

    reel_link = reel_link[-1]

    # Download reel
    download_bot = DownloadReel()
    await download_bot.download_reel_async(reel_link)

    # Post reel
    load_dotenv()

    for video in [
        vid
        for vid in os.listdir(os.getenv("REELS_PATH"))
        if vid.lower().endswith(".mp4")
    ]:
        full_vid_path = os.path.join(os.getenv("REELS_PATH"), video)
        await post_bot.post_reel(full_vid_path)
        os.remove(full_vid_path)
        try:
            os.remove(full_vid_path.replace('.mp4', '.txt'))
        except Exception as e:
            raise 'No txt file was found'
        print(f"Done: {full_vid_path}")

    await message.answer(f"Done")
