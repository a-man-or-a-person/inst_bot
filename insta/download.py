import os
import re

import instaloader
from dotenv import load_dotenv


class DownloadReel:
    def __init__(self):
        load_dotenv()
        os.makedirs(os.getenv("REELS_PATH"), exist_ok=True)

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

    def download_reel(self, reel_url):
        # Extract shortcode from URL
        print(reel_url)
        shortcode = re.search(r"(?:reels|p|reel)/([A-Za-z0-9_-]{10,12})", str(reel_url)).group(1)

        try:
            # Download the reel
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            self.loader.download_post(post, target=post.owner_username)
            print(f"✓ Downloaded: {post.owner_username}/{post.date_utc}.mp4")
        except Exception as e:
            print(f"Error: {e}")

