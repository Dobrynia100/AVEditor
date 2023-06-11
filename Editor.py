from pytube import YouTube
import os
import re
from moviepy.editor import *
import tkinter
from tkinter.messagebox import showerror, showwarning, askyesno
import customtkinter as ctk
import random
import json
import togif

def change_appearance_mode_event(new_appearance_mode: str):  # Function for the appearance change button
    ctk.set_appearance_mode(new_appearance_mode)


def change_language(new_language: str):  # Changing the UI language from a file
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
    convert_label.configure(text=lines[15])
    buttonV.configure(text=lines[4])
    buttonA.configure(text=lines[5])
    button_convert.configure(text=lines[6])
    button_convert_webm.configure(text=lines[14])
    entry1.configure(placeholder_text=lines[7])
    entry2.configure(placeholder_text=lines[8])
    errmsg.set(lines[9])
    errmsg2.set(lines[10])
    downl.set(lines[11])
    errmsg3.set(lines[12])
    errmsg4.set(lines[13])


def mp4tomp3():  # Converts mp4 file to mp3
    try:
        file_name = os.path.basename(entry2.get())
        file_name = file_name.split('.')[0]
        print(file_name)
        # print(os.path.split(video_path)[0])
        audio_path = os.path.split(entry2.get())[0] + '\\' + str(file_name) + '.mp3'
        print(audio_path)
        file_to_convert = AudioFileClip(entry2.get())
        file_to_convert.write_audiofile(audio_path)
        file_to_convert.close()
    except Exception as e:
        showerror(title="Error", message=(errmsg3.get(), e))


def mp4towebm():  # Converts mp4 file to webm
    try:
        file_name = os.path.basename(entry2.get())
        file_name = file_name.split('.')[0]
        print(file_name)
        webm_path = os.path.split(entry2.get())[0] + '\\' + str(file_name) + '.webm'
        print(webm_path)
        clip = VideoFileClip(entry2.get())
        clip.write_videofile(webm_path, codec='libvpx', audio_codec='libvorbis')
        clip.close()
    except Exception as e:
        showerror(title="Error", message=(errmsg3.get(), e))


def is_valid(link):  # Checks if the entered link is a youtube link
    Download_label.grid_forget()
    pattern = r'^https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)$'
    match = re.match(pattern, link)
    print(re.match(pattern, link))
    if match:
        buttonA.configure(state="normal")
        buttonV.configure(state="normal")
        error_label.grid_forget()
        return True
    else:
        error_label.grid(row=1, column=1, padx=20, pady=(5, 5))
        buttonA.configure(state="disabled")
        buttonV.configure(state="disabled")
        return False


def path_valid(path):  # Checks if the entered path is a path to folder or file
    print(path)
    print(os.path.isdir(path))
    print(os.path.exists(path))
    if os.path.isdir(path) or os.path.exists(path):
        error_label2.grid_forget()
        buttonA.configure(state="normal")
        buttonV.configure(state="normal")
        button_convert.configure(state="normal")
        button_convert_webm.configure(state="normal")
        app.geometry(f"{630}x{335}")
    else:
        error_label2.grid(row=4, column=1, padx=20, pady=5)
        app.geometry(f"{630}x{400}")  # app resolution
        buttonA.configure(state="disabled")
        buttonV.configure(state="disabled")
        button_convert.configure(state="disabled")
        button_convert_webm.configure(state="disabled")
    return os.path.isdir(path)


def button_video():  # downloads highest resolution video from youtube
    try:
        if random.random() <= 0.01:
            link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        else:
            link = entry1.get()

        yt = YouTube(link)  # , use_oauth=True, allow_oauth_cache=True)

        if yt.age_restricted:
            yt.bypass_age_gate()

        print("Title:", yt.title)
        load = yt.streams.get_highest_resolution()
        print('Video')
    except Exception as e:
        result = askyesno(title="Error",
                          message=errmsg4.get())  # "Video is age restricted, and can't be accessed without logging in")
        if result:
            yt = YouTube(link, use_oauth=True, allow_oauth_cache=False,on_complete_callback=compV)
            load = yt.streams.get_highest_resolution()
        load.download(entry2.get())
        print('Downloaded')


def button_audio():  # downloads only audio from youtube video
    try:
        link = entry1.get()
        yt = YouTube(link,
                     on_complete_callback=complete)  # ,use_oauth=True,  allow_oauth_cache=True,on_progress_callback=progress_func,on_complete_callback=complete)
        if yt.age_restricted:
            yt.bypass_age_gate()

        print("Title:", yt.title)
        load = yt.streams.get_audio_only()
        print('Audio')
        load.download(entry2.get())
        print('Downloaded')
    except Exception as e:
        showerror(title="Error", message=str(errmsg4.get(), str(e)))


def complete(stream, file_path):
    # print(file_path)
    file_to_convert = AudioFileClip(file_path)
    file_name = os.path.basename(file_path)
    file_name = file_name.split('.')[0]
    # print(file_name)
    audio_path = os.path.split(file_path)[0] + '\\' + str(file_name) + '.mp3'
    # print(audio_path)
    file_to_convert.write_audiofile(audio_path)
    file_to_convert.close()
    os.remove(file_path)
    Download_label.grid(row=2, column=0, padx=20, pady=5)


def compV(stream, file_path):
    Download_label.grid(row=2, column=0, padx=20, pady=5)

def gifmaker():
    togif.run()

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
app.geometry(f"{630}x{335}")  # app resolution

frame = ctk.CTkFrame(master=app)  # main background frame
frame.grid(row=0, column=1, rowspan=6, padx=(10, 20), pady=(20, 20), sticky="nsew")
frame.grid_rowconfigure(4, weight=1)

sidebar_frame = ctk.CTkFrame(master=app)  # frame for settings
sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
sidebar_frame.grid_rowconfigure(2, weight=1)

convert_frame = ctk.CTkFrame(master=app)
convert_frame.grid(row=6, column=1, rowspan=2, padx=(10, 20), pady=2, sticky="nsew")
convert_frame.grid_rowconfigure(1, weight=1)

errmsg = tkinter.StringVar()
errmsg2 = tkinter.StringVar()
errmsg3 = tkinter.StringVar()
errmsg4 = tkinter.StringVar()
downl = tkinter.StringVar()

button = ctk.CTkButton(master=app, text="Make a Gif", command=gifmaker)
button.grid(row=7, column=0, padx=20, pady=10)
# Sidebar
Download_label = ctk.CTkLabel(master=sidebar_frame, fg_color="transparent", textvariable=downl, wraplength=250)

appearance_mode_label = ctk.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

appearance_mode_optionemenu = ctk.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
appearance_mode_optionemenu.set("Dark")

language_label = ctk.CTkLabel(sidebar_frame, text="language", anchor="w")
language_label.grid(row=3, column=0, padx=20, pady=(10, 10))
language_options = ctk.CTkOptionMenu(sidebar_frame, values=["English", "Russian"], command=change_language)
language_options.grid(row=4, column=0, padx=20, pady=(10, 0))

button_Save = ctk.CTkButton(master=sidebar_frame, text="Save Settings", command=save_settings)
button_Save.grid(row=7, column=0, padx=20, pady=(10, 10))

# Main Frame

label1 = ctk.CTkLabel(master=frame, text="Insert link to a video from Youtube",
                      font=ctk.CTkFont(size=11, weight="bold"))  # Instruction label
label1.grid(row=0, column=1, padx=20, pady=(20, 10))

label2 = ctk.CTkLabel(master=frame, text="Download:", font=ctk.CTkFont(size=11, weight="bold"))
label2.grid(row=1, column=2, padx=10, pady=(5, 5))

error_label = ctk.CTkLabel(master=frame, fg_color="transparent", textvariable=errmsg,
                           wraplength=250)  # error label for incorrect youtube link

check = app.register(is_valid)  # checks if input is correct
entry1 = ctk.CTkEntry(master=frame, placeholder_text="Link", validate="focusout", validatecommand=(check, "%P"))
entry1.grid(row=2, column=1, padx=20, pady=10)

check2 = app.register(path_valid)
entry2 = ctk.CTkEntry(master=frame, placeholder_text="Save path", validate="focusout", validatecommand=(check2, "%P"))
entry2.grid(row=3, column=1, padx=20, pady=10)

error_label2 = ctk.CTkLabel(master=frame, fg_color="transparent", textvariable=errmsg2,
                            wraplength=250)  # error label for incorrect path

buttonV = ctk.CTkButton(master=frame, text="Video", command=button_video)  # button to download a Video
buttonV.grid(row=2, column=2, padx=20, pady=10)

buttonA = ctk.CTkButton(master=frame, text="Audio", command=button_audio)  # button to download a Audio
buttonA.grid(row=3, column=2, padx=20, pady=10)

# Convert Frame
convert_label=ctk.CTkLabel(master=convert_frame,fg_color="transparent",text="Convert",wraplength=110)
convert_label.grid(row=0,column=0)

button_convert = ctk.CTkButton(master=convert_frame, text="Convert to mp3",
                               command=mp4tomp3)  # button to convert mp4 to mp3
button_convert.grid(row=1, column=0, padx=20, pady=10)

button_convert_webm = ctk.CTkButton(master=convert_frame, text="Convert to webm", command=mp4towebm,
                                    height=37)  # button to convert mp4 to webm
button_convert_webm.grid(row=1, column=1, padx=20, pady=10)

settings()
app.resizable(False, False)
app.mainloop()
