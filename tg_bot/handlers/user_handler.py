import os

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dotenv import load_dotenv

from DB.orm import (add_ints_acc, add_link, create_tables, delete_link,
                    get_inst_accounts, get_links)
from insta.download import DownloadReel
from insta.post import AsyncPostReel
from tg_bot.fsm_classes import InstAccAdd

user_router = Router()
post_bot = AsyncPostReel()
load_dotenv()


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Приветствуем вас в нашем Боте! \n Присылайте ссылки на смешные ролики из инстаграмма."
    )


@user_router.message(F.text.contains("http"))
async def cmd_start(message: Message):
    reel_link = message.text.split("?")[0]
    await add_link(message.from_user.id, message.from_user.first_name, reel_link)
    await message.answer("Link added to DB. \n Thank you!")


@user_router.message(F.text.contains("Links"))
async def cmd_start(message: Message):
    await message.answer(f"Getting links...")
    await message.answer(str(await get_links()))


@user_router.message(F.text == "DB")
async def cmd_start(message: Message):
    await create_tables()
    await message.answer(f"Dropping tables")


@user_router.message(Command("post"))
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
    if os.getenv("TEST") == "True":
        await message.answer(f"Downloaded_passing to post")

    # Post reel
    # for video in [
    #     vid
    #     for vid in os.listdir(os.getenv("REELS_PATH"))
    #     if vid.lower().endswith(".mp4")
    # ]:
    video = [
        vid
        for vid in os.listdir(os.getenv("REELS_PATH"))
        if vid.lower().endswith(".mp4")
    ][0]

    full_vid_path = os.path.join(os.getenv("REELS_PATH"), video)
    res = await post_bot.post_reel(full_vid_path)
    if res[0]:
        try:
            os.remove(full_vid_path.replace(".mp4", ".txt"))
        except Exception as e:
            if os.getenv("TEST") == "True":
                print("No txt file was found")
        await message.answer(f"Done")
    else:
        await message.answer(f"Error: {res[1]}")


@user_router.message(F.text == "accounts")
async def get_accounts(message: Message):
    ans = await get_inst_accounts()
    ret_ans = 'id\t\t\tusername\t\n'
    for i in ans:
        ret_ans += f'{i[0]}\t\t\t{i[1]}\n'
    await message.answer(ret_ans)


@user_router.message(F.text == "add_acc")
async def get_film_code_from_user(message: Message, state: FSMContext):
    await message.answer("Отправьте Username")
    await state.set_state(InstAccAdd.username)


@user_router.message(InstAccAdd.username)
async def get_film_code_from_user(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(InstAccAdd.password)
    await message.answer("Отправьте password")


@user_router.message(InstAccAdd.password)
async def get_film_code_from_user(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await add_ints_acc(data, message.from_user.id)
    await message.answer("Аккаунт добавлен")
