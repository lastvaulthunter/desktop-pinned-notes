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

default_autosave_value_in_sec = 3

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

def apply_dark_theme_if_enabled():
    if dark_theme_enabled:
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        text_bg = "#3c3c3c"
        text_fg = "#ffffff"
        select_bg = "#4a4a4a"
        select_fg = "#ffffff"
        
        notes.config(
            bg=text_bg,
            fg=text_fg,
            insertbackground=fg_color, 
            selectbackground=select_bg,
            selectforeground=select_fg
        )
        
        root.config(bg=bg_color)
        
        style.configure('TFrame', background=bg_color)
        style.configure('Horizontal.TScale', 
                       background=bg_color,
                       foreground=fg_color,
                       troughcolor="#3c3c3c")
        style.configure('Vertical.TScrollbar',
                       background=bg_color,
                       troughcolor="#3c3c3c")
    else:
        # Apply light theme (default system colors)
        notes.config(
            bg="white",
            fg="black",
            insertbackground="black",
            selectbackground="#c0c0c0",
            selectforeground="black"
        )
        
        root.config(bg='SystemButtonFace')
        
        style.configure('TFrame', background='SystemButtonFace')
        style.configure('Horizontal.TScale', 
                       background='SystemButtonFace',
                       foreground='black',
                       troughcolor='SystemButtonFace')
        style.configure('Vertical.TScrollbar',
                       background='SystemButtonFace',
                       troughcolor='SystemButtonFace')

def save_notes():
    # Save notes to notes.txt
    with open(notesFile, "w") as f:
        notes_content = notes.get("1.0", "end-1c")
        f.write(notes_content)

    # Print current time and "saved" message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - Notes saved")

    # Schedule the next save after autosave_seconds
    root.after(autosave_seconds * 1000, save_notes)

def on_close():
    save_notes()  # Save notes before closing the app
    # Save window position and size to settings.json
    with open(settingsFile, "w") as f:
        settings = {
            "x": root.winfo_x(),
            "y": root.winfo_y(),
            "width": root.winfo_width(),
            "height": root.winfo_height(),
            "transparency": transparency_scale.get(),
            "autosave_seconds": autosave_seconds,
            "dark_theme": dark_theme_enabled
        }
        json.dump(settings, f)
    root.destroy()

def open_settings():
    global settings_window, theme_var, autosave_var
    
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x200")
    settings_window.resizable(False, False)
    settings_window.attributes('-topmost', True)
    
    x = root.winfo_x() + (root.winfo_width() // 2) - 150
    y = root.winfo_y() + (root.winfo_height() // 2) - 100
    settings_window.geometry(f"+{x}+{y}")
    
    theme_var = tk.BooleanVar(value=dark_theme_enabled)
    autosave_var = tk.IntVar(value=autosave_seconds)
    
    if dark_theme_enabled:
        settings_window.config(bg="#2b2b2b")
        label_bg = "#2b2b2b"
        label_fg = "#ffffff"
    else:
        settings_window.config(bg='SystemButtonFace')
        label_bg = 'SystemButtonFace'
        label_fg = 'black'
    
    frame = ttk.Frame(settings_window, padding="20")
    frame.pack(fill='both', expand=True)
    
    theme_frame = ttk.Frame(frame)
    theme_frame.pack(fill='x', pady=(0, 15))
    
    theme_label = tk.Label(theme_frame, text="Dark Theme:", bg=label_bg, fg=label_fg)
    theme_label.pack(side='left')
    
    theme_switch = ttk.Checkbutton(theme_frame, variable=theme_var)
    theme_switch.pack(side='right')
    
    autosave_frame = ttk.Frame(frame)
    autosave_frame.pack(fill='x', pady=(0, 15))
    
    autosave_label = tk.Label(autosave_frame, text="Autosave (seconds):", bg=label_bg, fg=label_fg)
    autosave_label.pack(side='left')
    
    autosave_spinbox = ttk.Spinbox(autosave_frame, from_=1, to=60, width=10, textvariable=autosave_var)
    autosave_spinbox.pack(side='right')
    
    buttons_frame = ttk.Frame(frame)
    buttons_frame.pack(fill='x', pady=(20, 0))
    
    save_button = ttk.Button(buttons_frame, text="Save", command=save_settings)
    save_button.pack(side='right', padx=(5, 0))
    
    cancel_button = ttk.Button(buttons_frame, text="Cancel", command=close_settings)
    cancel_button.pack(side='right')
    
    settings_window.transient(root)
    settings_window.grab_set()
    

def save_settings():
    global dark_theme_enabled, autosave_seconds
    
    new_dark_theme = theme_var.get()
    new_autosave_seconds = autosave_var.get()
    
    if new_dark_theme != dark_theme_enabled:
        dark_theme_enabled = new_dark_theme
        apply_dark_theme_if_enabled()
    
    autosave_seconds = new_autosave_seconds
    
    with open(settingsFile, "w") as f:
        settings = {
            "x": root.winfo_x(),
            "y": root.winfo_y(),
            "width": root.winfo_width(),
            "height": root.winfo_height(),
            "transparency": transparency_scale.get(),
            "autosave_seconds": autosave_seconds,
            "dark_theme": dark_theme_enabled
        }
        json.dump(settings, f)
    
    settings_window.destroy()
    print("Settings saved and applied")

def close_settings():
    settings_window.destroy()

# Load settings from settings.json or set default values
try:
    with open(settingsFile, "r") as f:
        settings = json.load(f)
    
    autosave_seconds = settings.get("autosave_seconds", 3)
    dark_theme_enabled = settings.get("dark_theme", False)
    
    if not isinstance(autosave_seconds, int):
        print(f"Warning: autosave_seconds is not int, using default value (3)")
        autosave_seconds = default_autosave_value_in_sec

except FileNotFoundError:
    # Create settings.json with default values
    settings = {
        "x": 0,
        "y": 180,
        "width": 950,
        "height": 800,
        "transparency": 100,
        "autosave_seconds": default_autosave_value_in_sec,
        "dark_theme": False
    }
    autosave_seconds = default_autosave_value_in_sec
    dark_theme_enabled = False

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
transparency_scale.pack(side='left', fill='x', expand=True, padx=(10,3), pady=5)

settings_image = tk.PhotoImage(file = r"icon_settings.png")
settings_image_resized = settings_image.subsample(5, 5)
settings_button = ttk.Button(frame_scale, text = 'Settings', image = settings_image_resized, command=open_settings)
settings_button.pack(side='right', padx=(5, 10), pady=5)

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

apply_dark_theme_if_enabled()

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

# Schedule the initial save after autosave_seconds
root.after(autosave_seconds * 1000, save_notes)

root.mainloop()