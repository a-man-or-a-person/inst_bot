from download import DownloadReel
from post import PostReel
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    selection = input('Download or post')
    if selection == 'd':
        download_bot = DownloadReel()
        download_bot.download_reel(input('Link for reel: '))
    elif selection == 'p':
        post_bot = PostReel()
        post_bot.post_reel()
    else:
        print('Wrong selection')
        
        