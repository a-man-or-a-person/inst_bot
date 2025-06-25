import instaloader
import re
import requests
from bs4 import BeautifulSoup


def download_reel(reel_url):
    # Extract shortcode from URL
    shortcode = re.search(r'(?:reels|p)/([A-Za-z0-9_-]{10,12})', reel_url).group(1)

    # Initialize Instaloader
    loader = instaloader.Instaloader(
        save_metadata=False,
        download_pictures=False,
        download_videos=True,
        download_geotags=False,
        download_comments=False,
        compress_json=False
    )

    try:
        # Download the reel
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=post.owner_username)
        print(f"✓ Downloaded: {post.owner_username}/{post.date_utc}.mp4")
    except Exception as e:
        print(f"Error: {e}")


# Example usage:
if __name__ == "__main__":
    # Get URL from user
    reel_url = input("Enter Instagram Reel URL: ").strip()

    # Validate URL format
    if not re.match(r'https?://(www\.)?instagram\.com/(reels|p)/', reel_url):
        print("Invalid URL. Must be an Instagram Reel link.")
    else:
        download_reel(reel_url)

import requests


def download_reel_no_login(reel_url):
    try:
        response = requests.get(reel_url)
        video_url = re.search(r'"video_url":"(https?://[^"]+)"', response.text).group(1)
        video_data = requests.get(video_url).content

        with open("instagram_reel.mp4", "wb") as f:
            f.write(video_data)
        print("✓ Downloaded: instagram_reel.mp4")
    except Exception as e:
        print(f"Error: {e}")