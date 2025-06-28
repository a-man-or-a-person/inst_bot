from download import DownloadReel
from post import PostReel
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    selection = input('Download or post')
    if selection == 'd':
        with open(r'C:\Users\User\Desktop\reel_download.txt', 'r') as file:
            hrefs = file.readlines()
            download_bot = DownloadReel()
            for link in hrefs:
                download_bot.download_reel(link)
    elif selection == 'p':
        load_dotenv()
        post_bot = PostReel()
        for video in os.listdir(os.getenv('REELS_PATH')):
            full_vid_path = os.path.join(os.getenv('REELS_PATH'), video)
            post_bot.post_reel(full_vid_path)
            os.remove(full_vid_path)
            print(f'Done: {full_vid_path}')
    else:
        print('Wrong selection')
        
        