from pytube import YouTube
from sys import argv
import os
print("download video(1) or audio(2)?")
link =argv[1]
yt = YouTube(link)

print("Title:",yt.title)
while():
    if input() == 1:
        downl=yt.streams.get_highest_resolution()
        break
    if input()==2:
        downl=yt.streams.get_audio_only()
        break
    else:
        print("wrong button")

path=input("Input path to download")
if os.path.isdir(path):
    downl.download(path)
else:
    print("The entered string is not a valid folder path or the folder does not exist")
