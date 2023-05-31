from pytube import YouTube
import os
from moviepy.editor import *

print("Insert link to a video from Youtube")
link = input()
yt = YouTube(link)
print("Title:",  yt.title)
inp = input("download video(1) or audio(2)?")
if float(inp)!= float(2):
    downl=yt.streams.get_highest_resolution()
    print('Video')
else:
    downl=yt.streams.get_audio_only()
    print('Audio')


path = input("Input path to download\n")
if os.path.isdir(path):
    downl.download(path)
    print('Downloaded')
else:
    print("The entered string is not a valid folder path or the folder does not exist")
