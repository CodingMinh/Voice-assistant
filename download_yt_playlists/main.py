# pip install pytubefix
import re
from pytubefix import Playlist
playlist = Playlist('https://www.youtube.com/playlist?list=PLPhXtbZry9Db9q4fsvVS1KVSWHt43g4cX')   
DOWNLOAD_DIR = 'D:\Songs' # download directory, will create a new folder if that folder doesn't exist
playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")    
print(len(playlist.video_urls))    
for url in playlist.video_urls:
    print(url)    
for video in playlist.videos:
    print('downloading : {} with url : {}'.format(video.title, video.watch_url))
    video.streams.\
        filter(type='video', progressive=True, file_extension='mp4').\
        order_by('resolution').\
        desc().\
        first().\
        download(DOWNLOAD_DIR)