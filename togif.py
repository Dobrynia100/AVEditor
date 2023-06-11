import os
import re
from moviepy.editor import *
import tkinter
from tkinter.messagebox import showerror, showwarning, askyesno
import customtkinter as ctk
import moviepy.video.fx.all as vfx


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

    # label1.configure(text="Make a gif")
    label2.configure(text=lines[17])
    entry1.configure(placeholder_text=lines[18])
    button_gif.configure(text=lines[19])
    add_text.configure(text=lines[20])
    entry2.configure(placeholder_text=lines[21])
    entry3.configure(placeholder_text=lines[22])
    loop_switch.configure(values=[lines[23], lines[24]], font=("Ariel", 15), width=250, height=45)


def time_symetrize(clip):  # Returns a clip that is time-symmetrized by concatenating the original clip with
    # its time-reversed version.
    return concatenate([clip, clip.fx(vfx.time_mirror)])


def fade_in(clip):  # Applies a fade-in effect to the input clip by crossfading it from transparent
    # to opaque over half of its duration.
    d = clip.duration
    clip = clip.crossfadein(d / 2)

    composition = (CompositeVideoClip([clip,
                                       clip.set_start(d / 2),
                                       clip.set_start(d)])
                   .subclip(d / 2, 3 * d / 2))
    return composition


def makegif():  # Function to create a GIF from a video clip with optional effects.
    file_name = os.path.basename(entry1.get())
    file_name = file_name.split('.')[0]
    clip = (VideoFileClip(entry1.get(), audio=False)
            .resize(0.6))
    if loop_switch.get() == "Time-symetrization":
        print("Time-symetrization")
        clip.fx(time_symetrize)
    elif loop_switch.get() == "Fade in":
        print("Fade in")
        clip = fade_in(clip)
    if (add_text.get() == "on"):
        clip = text_edit(clip)
    clip.write_gif(f"{file_name}.gif", program='imageio', fuzz=2, opt='wu')
    clip.close()


def path_valid(path):  # Checks if the entered path is a path to folder or file
    print(path)
    print(os.path.isdir(path))
    print(os.path.exists(path))

    if os.path.isdir(path) or os.path.exists(path):
        button_gif.configure(state="normal")
    else:
        button_gif.configure(state="disabled")

        # label1.configure(text=f"Duration:{clip.duration}")
    return os.path.isdir(path)


def run():  # Function to set up and run the application GUI.
    frame.grid(row=0, column=1, rowspan=2, padx=5, sticky="nsew")
    frame.grid_rowconfigure(4, weight=1)
    text_frame.grid(row=2, column=0, rowspan=2, padx=5, pady=5, sticky="nsew")
    entry1.grid(row=0, padx=10, pady=(10, 10), sticky="nsew", columnspan=2)
    add_text.grid(row=1, column=0, padx=5)
    font_menu.grid(row=2, column=0, padx=5)
    color_menu.grid(row=2, column=1, padx=5, pady=(10, 10))
    entry2.grid(row=3, column=0, padx=20, pady=10)
    entry3.grid(row=3, column=1, padx=0, pady=10)
    label2.grid(row=4, column=0, padx=10, pady=(5, 5), columnspan=2)
    loop_switch.grid(row=5, column=0, padx=10, pady=5, columnspan=2)
    button_gif.grid(row=7, column=0, padx=20, pady=10, sticky="nsew", columnspan=2)

    app.resizable(False, False)
    app.mainloop()


def text_edit(clip):  # Adds text to the input video clip.
    pos_x = entry2.get().split(',')[0]
    pos_y = entry2.get().split(',')[1]
    print(pos_x)
    print(pos_y)
    text = (TextClip(entry3.get(),
                     fontsize=30, color=color_menu.get(),
                     font=font_menu.get(), interline=-25)
            .set_pos((pos_x, pos_y))
            .set_duration(clip.duration))

    composition = CompositeVideoClip([clip, text])

    return composition


def enable_all_widgets():  # Enables or disables all widgets based on the state of the "Add text" checkbox.
    print(add_text.get())
    for child in text_frame.winfo_children():
        if (add_text.get() == "on"):
            child.configure(state='normal')
        else:
            child.configure(state='disabled')


# def on_closing():
#     app.protocol("WM_DELETE_WINDOW")

app = ctk.CTk()
app.title("AVEditor")
app.geometry(f"{350}x{330}")  # app resolution

frame = ctk.CTkFrame(master=app)  # main background frame

text_frame = ctk.CTkFrame(master=frame)

# Main Frame

label2 = ctk.CTkLabel(master=frame, text="Loop method:", font=ctk.CTkFont(size=11, weight="bold"))

check = app.register(path_valid)  # checks if input is correct

entry1 = ctk.CTkEntry(master=frame, placeholder_text="Path to mp4 file", validate="focusout",
                      validatecommand=(check, "%P"))

button_gif = ctk.CTkButton(master=frame, text="Make a Gif", command=makegif)  # button to download a Video

add_text = ctk.CTkCheckBox(master=frame, text="Add text", onvalue="on", offvalue="off", command=enable_all_widgets)

font_menu = ctk.CTkOptionMenu(master=text_frame, state="disabled", values=["Comic Sans", "Ariel", "Amiri-Bold"])
color_menu = ctk.CTkOptionMenu(master=text_frame, state="disabled", values=["white", "black"])

entry2 = ctk.CTkEntry(master=text_frame, state="disabled", placeholder_text="Position x,y", validate="focusout")
entry3 = ctk.CTkEntry(master=text_frame, state="disabled", placeholder_text="Text")

loop_switch = ctk.CTkSegmentedButton(master=frame, values=["Fade in", "Time-symetrization"])

# app.protocol("WM_DELETE_WINDOW",on_closing)
