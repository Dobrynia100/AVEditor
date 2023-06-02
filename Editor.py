from pytube import YouTube
import os
import re
from moviepy.editor import *
import tkinter
import customtkinter as ctk

def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)

def change_language(new_language:str):
    print(new_language)
    if new_language=="English":
        file=open("Eng_language","r")
        lines = file.readlines()
    else:
        with open('Ru_language', 'r', encoding='utf-8') as file:
            lines = file.readlines()
    label1.configure(text=lines[0])
    label2.configure(text=lines[1])
    appearance_mode_label.configure(text=lines[2])
    language_label.configure(text=lines[3])
    buttonV.configure(text=lines[4])
    buttonA.configure(text=lines[5])
    button_convert.configure(text=lines[6])
    entry1.configure(placeholder_text=lines[7])
    entry2.configure(placeholder_text=lines[8])
    errmsg = tkinter.StringVar()
    errmsg2 = tkinter.StringVar()
    error_label.configure(textvariable=errmsg.set(lines[9]))
    error_label2.configure(textvariable=errmsg2.set(lines[10]))
    file.close

def MP4ToMP3():
    file_name = os.path.basename(entry2.get())
    file_name = file_name.split('.')[0]
    print(file_name)
    # print(os.path.split(video_path)[0])
    audio_path = os.path.split(entry2.get())[0] + '\\' + file_name + '.mp3'
    print(audio_path)
    FILETOCONVERT = AudioFileClip(entry2.get())
    FILETOCONVERT.write_audiofile(audio_path)
    FILETOCONVERT.close()


def is_valid(link):
    pattern = r'^https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)$'
    match = re.match(pattern, link)
    print(re.match(pattern, link))
    if match:
        buttonA.configure(state="normal")
        buttonV.configure(state="normal")
        errmsg.set("")
        return True
    else:
        errmsg.set("Unvalid Youtube link")
        buttonA.configure(state="disabled")
        buttonV.configure(state="disabled")
        return False

def path_valid(path):
    print(os.path.isdir(path))
    if os.path.isdir(path):
        errmsg2.set("")
        buttonA.configure(state="normal")
        buttonV.configure(state="normal")
        button_convert.configure(state="normal")
    else:
        errmsg2.set("The entered string is not a valid folder path or the folder does not exist")
        buttonA.configure(state="disabled")
        buttonV.configure(state="disabled")
        button_convert.configure(state="disabled")
    return os.path.isdir(path)

def button_Video():
    link = entry1.get()
    yt = YouTube(link)
    print("Title:", yt.title)
    downl = yt.streams.get_highest_resolution()
    print('Video')
    downl.download(entry2.get())
    print('Downloaded')

def button_Audio():
    link = entry1.get()
    yt = YouTube(link)
    print("Title:", yt.title)
    downl = yt.streams.get_audio_only()
    print('Audio')
    downl.download(entry2.get())
    print('Downloaded')


def cut(event):
    print(event)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
default_lang="English"

app=ctk.CTk()
app.title("AVEditor")
app.geometry(f"{620}x{325}")

frame=ctk.CTkFrame(master=app)
frame.grid(row=0, column=1, rowspan=4, padx=(10, 20), pady=(20, 20),sticky="nsew")
frame.grid_rowconfigure(4, weight=1)

sidebar_frame = ctk.CTkFrame(master=app,width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)


errmsg= tkinter.StringVar()
errmsg2 = tkinter.StringVar()


label1=ctk.CTkLabel(master=frame,text="Insert link to a video from Youtube",font=ctk.CTkFont(size=11, weight="bold"))
label1.grid(row=0, column=1, padx=20, pady=(20, 10))

label2=ctk.CTkLabel(master=frame,text="Download:",font=ctk.CTkFont(size=11, weight="bold"))
label2.grid(row=1, column=2, padx=10, pady=(5, 5))

appearance_mode_label = ctk.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = ctk.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
appearance_mode_optionemenu.set("Dark")

language_label=ctk.CTkLabel(sidebar_frame,text="language",anchor="w")
language_label.grid(row=3,column=0,padx=20,pady=(10,0))
language_options=ctk.CTkOptionMenu(sidebar_frame,values=["English","Russian"],command=change_language)
language_options.grid(row=4, column=0, padx=20, pady=(10, 10))

buttonV = ctk.CTkButton(master=frame, text="Video", command=button_Video)
buttonV.grid(row=2, column=2,padx=20, pady=10)

buttonA = ctk.CTkButton(master=frame, text="Audio", command=button_Audio)
buttonA.grid(row=3, column=2,padx=20, pady=10)

button_convert=ctk.CTkButton(master=frame,text="Convert to mp3",command=MP4ToMP3)
button_convert.grid(row=5, column=1, padx=20, pady=4)

error_label = ctk.CTkLabel(master=frame,fg_color="transparent", textvariable=errmsg, wraplength=250)
error_label.grid(row=1, column=1, padx=20, pady=(5, 5))

check=app.register(is_valid)
entry1=ctk.CTkEntry(master=frame,placeholder_text="Link",validate="focusout",validatecommand=(check,"%P"))
entry1.grid(row=2, column=1,padx=20, pady=10)


check2=app.register(path_valid)
entry2=ctk.CTkEntry(master=frame,placeholder_text="Save path",validate="focusout",validatecommand=(check2,"%P"))
entry2.grid(row=3, column=1,padx=20, pady=10)


error_label2 = ctk.CTkLabel(master=frame, fg_color="transparent", textvariable=errmsg2, wraplength=250)
error_label2.grid(row=4, column=1, padx=20, pady=5)
change_language(default_lang)


app.mainloop()
