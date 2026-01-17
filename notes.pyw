# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 lastvaulthunter <lastvaulthunter@gmail.com>

import tkinter as tk
from tkinter import ttk, Text
import json
from datetime import datetime
import sys, os

# TODO:
# - pin/unpin
# - scroll bar on width?
# * tabs?
# * themed ttk - change
# - full window remember
# - html on/off
# - save/settings buttons
# - CTRL+Z ???


pyFile = sys.argv[0]
pyPath = os.path.dirname(pyFile) + "\\"
print(pyPath)

notesFile = pyPath + "notes.txt"
print(notesFile)

settingsFile = pyPath + "settings.json"
print(settingsFile)


def set_transparency(value):
    alpha_value = int(float(value))
    root.attributes("-alpha", alpha_value / 100)

def save_notes():
    # Save notes to notes.txt
    with open(notesFile, "w") as f:
        notes_content = notes.get("1.0", "end-1c")
        f.write(notes_content)

    # Print current time and "saved" message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - Notes saved")

    # Schedule the next save after 1 minute (60000 milliseconds)
    root.after(60000, save_notes)

def on_close():
    save_notes()  # Save notes before closing the app
    # Save window position and size to settings.json
    with open(settingsFile, "w") as f:
        settings = {
            "x": root.winfo_x(),
            "y": root.winfo_y(),
            "width": root.winfo_width(),
            "height": root.winfo_height(),
            "transparency": transparency_scale.get()
        }
        json.dump(settings, f)
    root.destroy()

# Load settings from settings.json or set default values
try:
    with open(settingsFile, "r") as f:
        settings = json.load(f)
except FileNotFoundError:
    # Create settings.json with default values
    settings = {
        "x": 0,
        "y": 180,
        "width": 950,
        "height": 800,
        "transparency": 100
    }
    with open(settingsFile, "w") as f:
        json.dump(settings, f)

root = tk.Tk()
root.geometry(f"{settings['width']}x{settings['height']}+{settings['x']}+{settings['y']}")
root.attributes("-alpha", settings["transparency"] / 100)
root.attributes('-topmost', True)

# Remove default Tkinter icon
root.iconbitmap(default="")

style = ttk.Style(root)
style.configure('TFrame', background='SystemButtonFace')

frame_scale = ttk.Frame(root, height=30)
frame_scale.pack(fill='x')

transparency_scale = ttk.Scale(frame_scale, from_=50, to=100, orient="horizontal", length=200, command=set_transparency)
transparency_scale.set(settings["transparency"])
transparency_scale.pack(side='top', fill='x', padx=10, pady=5)

frame_text = ttk.Frame(root)
frame_text.pack(fill='both', expand=True, padx=10, pady=10)

notes = Text(frame_text, wrap=tk.WORD)
notes.pack(fill='both', expand=True, side='left')

# Add a ttk vertical scrollbar to the right of the Text widget
scrollbar = ttk.Scrollbar(frame_text, command=notes.yview)
scrollbar.pack(side="right", fill="y")
notes.config(yscrollcommand=scrollbar.set)

# Load notes from notes.txt or create the file if not found
try:
    with open(notesFile, "r") as f:
        notes_content = f.read()
        notes.insert("1.0", notes_content)
except FileNotFoundError:
    with open(notesFile, "w") as f:
        pass  # Create an empty notes.txt file

# Bind the on_close function to the window close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Enable copy/paste functionality on not English keyboard layout (Ctrl+C and Ctrl+V + Ctrl+X)
def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

notes.bind_all("<Key>", _onKeyRelease, "+")



root.title("Notes")  # Set the title to "Notes"
root.minsize(150, 75) # Width, Height

# Schedule the initial save after 1 minute
root.after(60000, save_notes)

root.mainloop()
