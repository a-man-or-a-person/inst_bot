import asyncio
import os
import re
from concurrent.futures import ThreadPoolExecutor, TimeoutError

import instaloader
from dotenv import load_dotenv


class DownloadReel:
    def __init__(self):
        load_dotenv()
        os.makedirs(os.getenv("REELS_PATH"), exist_ok=True)

        self.executor = ThreadPoolExecutor()

        self.loader = instaloader.Instaloader(
            save_metadata=False,
            download_pictures=False,
            download_videos=True,
            download_geotags=False,
            download_comments=False,
            compress_json=False,
            download_video_thumbnails=False,
            dirname_pattern=os.getenv("REELS_PATH"),
        )

    async def download_reel_async(self, reel_url: str, timeout: int = 30):
        loop = asyncio.get_running_loop()

        try:
            # Add timeout to prevent hanging
            return await asyncio.wait_for(
                loop.run_in_executor(self.executor, self._download_reel_sync, reel_url),
                timeout=timeout,
            )
        except TimeoutError:
            return f"Timeout downloading {reel_url}"
        except instaloader.exceptions.InstaloaderException as e:
            return f"Instagram error: {str(e)}"

    def _download_reel_sync(self, reel_url: str):
        # Extract shortcode from URL
        shortcode = re.search(
            r"(?:reels|p|reel)/([A-Za-z0-9_-]{10,12})", str(reel_url)
        ).group(1)

        try:
            # Download the reel
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            self.loader.download_post(post, target=post.owner_username)
            print(f"✓ Downloaded: {post.owner_username}/{post.date_utc}.mp4")
        except Exception as e:
            print(f"Error: {e}")
