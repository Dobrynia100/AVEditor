from pytube import YouTube
import os
import re
from moviepy.editor import *
import tkinter
from tkinter import messagebox
import customtkinter as ctk
import random
import json

def change_appearance_mode_event(new_appearance_mode: str): # Function for the appearance change button
    ctk.set_appearance_mode(new_appearance_mode)



def change_language(new_language: str): # Changing the UI language from a file
    print(new_language)
    if new_language == "English":
        file = open("Eng_language", "r")
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
    errmsg3.set(lines[9])
    errmsg4.set(lines[10])

    file.close


def MP4ToMP3(): #Converts mp4 file to mp3
    try:
        file_name = os.path.basename(entry2.get())
        file_name = file_name.split('.')[0]
        print(file_name)
        # print(os.path.split(video_path)[0])
        audio_path = os.path.split(entry2.get())[0] + '\\' + file_name + '.mp3'
        print(audio_path)
        FILETOCONVERT = AudioFileClip(entry2.get())
        FILETOCONVERT.write_audiofile(audio_path)
        FILETOCONVERT.close()
    except Exception as e:
        messagebox.ERROR(title="Error",message=("Error while converting:", e))


def is_valid(link): # Checks if the entered link is a youtube link
    pattern = r'^https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)$'
    match = re.match(pattern, link)
    print(re.match(pattern, link))
    temp = errmsg3.get()
    if match:
        buttonA.configure(state="normal")
        buttonV.configure(state="normal")
        errmsg.set("")
        return True
    else:
        errmsg.set(temp)
        buttonA.configure(state="disabled")
        buttonV.configure(state="disabled")
        return False


def path_valid(path):# Checks if the entered path is a path to folder or file
    print(os.path.isdir(path))
    temp = errmsg4.get()
    if os.path.isdir(path):
        errmsg2.set("")
        buttonA.configure(state="normal")
        buttonV.configure(state="normal")
        button_convert.configure(state="normal")
    else:
        errmsg2.set(temp)
        buttonA.configure(state="disabled")
        buttonV.configure(state="disabled")
        button_convert.configure(state="disabled")
    return os.path.isdir(path)


def button_Video(): # downloads highest resolution video from youtube
    link = entry1.get()
    yt = YouTube(link,on_progress_callback=progress_func)
    if yt.age_restricted:
        yt.bypass_age_gate()
    print("Title:", yt.title)
    downl = yt.streams.get_highest_resolution()
    print('Video')
    downl.download(entry2.get())
    print('Downloaded')


def button_Audio(): #downloads only audio from youtube video
    try:
        if random.random()<=0.01:
            link="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        else:
            link = entry1.get()
        bar.grid(row=5, column=1, padx=10, pady=4)
        bar.set(0)
        yt = YouTube(link,on_progress_callback=progress_func,on_complete_callback=complete)#,use_oauth=True,  allow_oauth_cache=True,on_progress_callback=progress_func,on_complete_callback=complete)
        if yt.age_restricted:
          yt.bypass_age_gate()
          #dialog=ctk.CTkToplevel(text="Please open https://www.google.com/device and input code \n Press enter when you have completed this step.")
      # stream = yt.streams.get_audio_only()
       # stream.download(output_path=entry2.get(),filename=stream.default_filename,on_progress_callback=progress_func)
        print("Title:", yt.title)
        downl = yt.streams.get_audio_only()
        print('Audio')
        downl.download(entry2.get())
        print('Downloaded')
        bar.grid_forget()
        errmsg2.grid_forget()
    except Exception as e:
        messagebox.ERROR(title="Error",message=("Error while downloading:", e))

def complete(stream,file_path):
    print(file_path)
    FILETOCONVERT = AudioFileClip(file_path)
    file_name = os.path.basename(file_path)
    file_name = file_name.split('.')[0]
    print(file_name)
    audio_path = os.path.split(file_path)[0] + '\\' + file_name + '.mp3'
    print(audio_path)
    FILETOCONVERT.write_audiofile(audio_path)
    FILETOCONVERT.close()
    os.remove(file_path)
    errmsg2.set("Downloaded")

def progress_func(stream, chunk, bytes_remaining):
     #total_size = stream.filesize
     #bytes_downloaded = total_size - bytes_remaining
     n = 500
     iter_step = 1 / n
     progress_step = iter_step
     bar.start()
     for x in range(500):
         bar.set(progress_step)
         progress_step += iter_step
         app.update()
     bar.stop()
    # print(bytes_downloaded)
    # progress = int((bytes_downloaded / total_size) * 100)
    # print(progress)
    # print(bar.get())
    # bar.set(0)
    # print(bar.get())
    # bar.start()
    #bar.set(bar.get()+len(chunk))
    #bar.step()

def settings():
    print("Loading settings")
    with open('Config.json', 'r') as file:
        settings_data = file.read()
    settings = json.loads(settings_data)

    change_language(settings["language"])
    language_options.set(settings["language"])
    change_appearance_mode_event(settings["appearance_mode"])
    appearance_mode_optionemenu.set(settings["appearance_mode"])

def save_settings():
    new_settings = {
        "language": language_options.get(),
        "appearance_mode": appearance_mode_optionemenu.get()
    }

    with open('Config.json', 'w') as file:
        json.dump(new_settings, file)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


app = ctk.CTk()
app.title("AVEditor")
app.geometry(f"{660}x{335}") #app resolution

frame = ctk.CTkFrame(master=app) #main background frame
frame.grid(row=0, column=1, rowspan=4, padx=(10, 20), pady=(20, 20), sticky="nsew")
frame.grid_rowconfigure(4, weight=1)

sidebar_frame = ctk.CTkFrame(master=app, width=140, corner_radius=0) # frame for settings
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)

errmsg = tkinter.StringVar()
errmsg2 = tkinter.StringVar()
errmsg3 = tkinter.StringVar()
errmsg4 = tkinter.StringVar()


label1 = ctk.CTkLabel(master=frame, text="Insert link to a video from Youtube",
                      font=ctk.CTkFont(size=11, weight="bold")) #Instruction label
label1.grid(row=0, column=1, padx=20, pady=(20, 10))

label2 = ctk.CTkLabel(master=frame, text="Download:", font=ctk.CTkFont(size=11, weight="bold"))
label2.grid(row=1, column=2, padx=10, pady=(5, 5))

appearance_mode_label = ctk.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = ctk.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10))
appearance_mode_optionemenu.set("Dark")

language_label = ctk.CTkLabel(sidebar_frame, text="language", anchor="w")
language_label.grid(row=3, column=0, padx=20, pady=(10, 0))
language_options = ctk.CTkOptionMenu(sidebar_frame, values=["English", "Russian"], command=change_language)
language_options.grid(row=4, column=0, padx=20, pady=(10, 10))

buttonV = ctk.CTkButton(master=frame, text="Video", command=button_Video)#button to download a Video
buttonV.grid(row=2, column=2, padx=20, pady=10)

buttonA = ctk.CTkButton(master=frame, text="Audio", command=button_Audio)#button to download a Audio
buttonA.grid(row=3, column=2, padx=20, pady=10)

button_convert = ctk.CTkButton(master=frame, text="Convert to mp3", command=MP4ToMP3)#button to convert mp4 to mp3
button_convert.grid(row=5, column=2, padx=20, pady=4)

button_Save=ctk.CTkButton(master=sidebar_frame,text="Save Settings",command=save_settings)
button_Save.grid(row=6, column=0, padx=20, pady=(10, 10))

error_label = ctk.CTkLabel(master=frame, fg_color="transparent", textvariable=errmsg, wraplength=250)#error label for incorrect youtube link
error_label.grid(row=1, column=1, padx=20, pady=(5, 5))

check = app.register(is_valid) # checks if input is correct
entry1 = ctk.CTkEntry(master=frame, placeholder_text="Link", validate="focusout", validatecommand=(check, "%P"))
entry1.grid(row=2, column=1, padx=20, pady=10)

check2 = app.register(path_valid)
entry2 = ctk.CTkEntry(master=frame, placeholder_text="Save path", validate="focusout", validatecommand=(check2, "%P"))
entry2.grid(row=3, column=1, padx=20, pady=10)

error_label2 = ctk.CTkLabel(master=frame, fg_color="transparent", textvariable=errmsg2, wraplength=250)#error label for incorrect path
error_label2.grid(row=4, column=1, padx=20, pady=5)

bar=ctk.CTkProgressBar(master=frame,width=100)

settings()

app.mainloop()
