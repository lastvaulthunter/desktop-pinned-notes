import tkinter as tk
from tkinter import ttk, Text
import json
from datetime import datetime

def set_transparency(value):
    alpha_value = int(float(value))
    root.attributes("-alpha", alpha_value / 100)

def save_notes():
    # Save notes to notes.txt
    with open("notes.txt", "w") as f:
        notes_content = notes.get("1.0", "end-1c")
        f.write(notes_content)

    # Print current time and "saved" message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - Notes saved")

def on_close():
    # Save window position and size to settings.json
    with open("settings.json", "w") as f:
        settings = {
            "x": root.winfo_x(),
            "y": root.winfo_y(),
            "width": root.winfo_width(),
            "height": root.winfo_height(),
            "transparency": transparency_scale.get()
        }
        json.dump(settings, f)

    save_notes()  # Save notes before closing the app
    root.destroy()

# Load settings from settings.json or set default values
try:
    with open("settings.json", "r") as f:
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
    with open("settings.json", "w") as f:
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
notes.pack(fill='both', expand=True)

# Load notes from notes.txt or create the file if not found
try:
    with open("notes.txt", "r") as f:
        notes_content = f.read()
        notes.insert("1.0", notes_content)
except FileNotFoundError:
    with open("notes.txt", "w") as f:
        pass  # Create an empty notes.txt file

# Bind the on_close function to the window close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Bind the save_notes function to the FocusOut event of the Text widget
notes.bind("<FocusOut>", lambda event: save_notes())

root.title("Notes")  # Set the title to "Notes"

root.mainloop()
