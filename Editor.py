from pytube import YouTube
import os
from moviepy.editor import *

def MP4ToMP3():
    video_path = input("Insert part to .mp4")
    print(video_path)
    file_name = os.path.basename(video_path)
    file_name = file_name.split('.')[0]
    print(file_name)
    # print(os.path.split(video_path)[0])
    audio_path = os.path.split(video_path)[0] + '\\' + file_name + '.mp3'
    print(audio_path)
    FILETOCONVERT = AudioFileClip(video_path)
    FILETOCONVERT.write_audiofile(audio_path)
    FILETOCONVERT.close()

def downloading():
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

inp=input("download(1) or convert(2)")
if float(inp)==1:
    downloading()
elif float(inp)==2:
    MP4ToMP3()

