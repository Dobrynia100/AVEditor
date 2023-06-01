from pytube import YouTube
import os
import re
from moviepy.editor import *
import tkinter
import customtkinter as ctk

def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)

def MP4ToMP3():
    video_path = input("Insert part to .mp4\n")
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


def is_valid(link):
    pattern = r'^https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)$'
    match = re.match(pattern, link)
    print(re.match(pattern, link))
    if match:
        buttonA.configure(state="normal")
        buttonV.configure(state="normal")
        errmsg.set("")
    else:
        errmsg.set("Unvalid Youtube link")
        buttonA.configure(state="disabled")
        buttonV.configure(state="disabled")
    return match

def path_valid(path):
    print(os.path.isdir(path))
    if os.path.isdir(path):
        errmsg2.set("")
        buttonA.configure(state="normal")
        buttonV.configure(state="normal")
    else:
        errmsg2.set("The entered string is not a valid folder path or the folder does not exist")
        buttonA.configure(state="disabled")
        buttonV.configure(state="disabled")
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

app=ctk.CTk()
app.title("AVEditor")
app.geometry(f"{500}x{350}")

app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0, 1, 2), weight=1)

frame=ctk.CTkFrame(master=app)
#frame.pack(pady=20,padx=60,fill="both",expand=True)
frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
frame.grid_rowconfigure(4, weight=1)

errmsg = tkinter.StringVar()
errmsg2 = tkinter.StringVar()
label1=ctk.CTkLabel(master=frame,text="Insert link to a video from Youtube",font=ctk.CTkFont(size=11, weight="bold"))
#label1.pack(pady=10,padx=10,anchor=tkinter.W)
label1.grid(row=0, column=0, padx=20, pady=(20, 10))

buttonV = ctk.CTkButton(master=frame, text="Video", command=button_Video)
#buttonV.pack(pady=10,padx=10,anchor=tkinter.E)
buttonV.grid(row=2, column=1,padx=20, pady=10)

buttonA = ctk.CTkButton(master=frame, text="Audio", command=button_Audio)
#buttonA.pack(pady=10,padx=10, anchor=tkinter.E)
buttonA.grid(row=3, column=1,padx=20, pady=10)
error_label = ctk.CTkLabel(master=frame,fg_color="transparent", textvariable=errmsg, wraplength=250)
#error_label.place(relx=0.5, rely=0.5, anchor=tkinter.NW)
error_label.grid(row=1, column=0, padx=20, pady=(5, 5))

check=app.register(is_valid)
entry1=ctk.CTkEntry(master=frame,placeholder_text="Link",validate="key",validatecommand=(check,"%P"))
#entry1.place(relx=0.1, rely=0.3,anchor=tkinter.W)
entry1.grid(row=2, column=0,padx=20, pady=10)
entry1.bind("<KeyPress>", is_valid(entry1.get()))

check2=app.register(path_valid)
entry2=ctk.CTkEntry(master=frame,placeholder_text="Save path",validate="key",validatecommand=(check2,"%P"))
#entry2.place(relx=0.1, rely=0.4,anchor=tkinter.W)
entry2.grid(row=3, column=0,padx=20, pady=10)
entry2.bind("<KeyPress>", path_valid(entry2.get()))

error_label2 = ctk.CTkLabel(master=frame, fg_color="transparent", textvariable=errmsg2, wraplength=250)
#error_label.place(relx=0.5, rely=0.5, anchor=tkinter.NW)
error_label2.grid(row=4, column=0, padx=20, pady=5)


app.mainloop()
