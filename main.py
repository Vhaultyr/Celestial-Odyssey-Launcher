import customtkinter as ctk
import tkinter.filedialog as filedialog
import configparser
import subprocess
from tkinter import messagebox
from PIL import Image  # Only need Image from PIL
import os

# Initialize the app
app = ctk.CTk()
app.title("Celestial Odyssey Launcher")
app.geometry("1024x576")
app.resizable(width=False, height=False)

# --- Config File Setup ---
config = configparser.ConfigParser()
config_file = "launcher_config.ini"

def load_config():
    if os.path.exists(config_file):
        config.read(config_file)
        return config.get('Settings', 'LastValidPath', fallback="")
    return ""

def save_config(path):
    config['Settings'] = {'LastValidPath': path}
    with open(config_file, 'w') as f:
        config.write(f)

# --- Enhanced Validation ---
def is_valid_minecraft_dir(path):
    """Check for common Minecraft installation markers"""
    if not path:  # Empty path
        return False
        
    required_markers = [
        os.path.join(path, "mods"),          # Forge/Fabric
        os.path.join(path, "versions"),      # Vanilla
        os.path.join(path, "resourcepacks")  # Resource packs
    ]
    return any(os.path.isdir(marker) for marker in required_markers)


# Load Assets
def load_image(path, size):
    try:
        img = Image.open(path)  # Get PIL Image
        # Convert to CTkImage (proper CustomTkinter format)
        return ctk.CTkImage(light_image=img, size=size)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

# Background
bg_image = load_image("assets/bg.png", (1024, 576))
if bg_image:
    bg_label = ctk.CTkLabel(app, image=bg_image, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    app.configure(fg_color="#2b2b2b")  # Fallback color

# Icon
if os.path.exists("assets/icon.ico"):
    app.iconbitmap("assets/icon.ico")


# --- News Panel ---
news_frame = ctk.CTkFrame(app, width=350, height=400, corner_radius=10)
news_frame.place(relx=0.05, rely=0.1, anchor="nw")
news_textbox = ctk.CTkTextbox(news_frame, width=330, height=350, wrap="word")
news_textbox.pack(padx=10, pady=10)
news_textbox.insert("1.0", "• Select a valid Minecraft folder\n• Folder must contain /mods directory")
news_textbox.configure(state="disabled")

# --- Version Selector ---
version_frame = ctk.CTkFrame(app, width=300, corner_radius=10)
version_frame.place(relx=0.7, rely=0.1, anchor="nw")
ctk.CTkLabel(version_frame, text="Select Version").pack(pady=5)
version_dropdown = ctk.CTkOptionMenu(version_frame, values=["Ultra", "Low"])
version_dropdown.pack(pady=10)

# --- Directory Browser with Validation ---
current_dir = ctk.StringVar(value=load_config() or "No folder selected")
dir_frame = ctk.CTkFrame(app)
dir_frame.place(relx=0.7, rely=0.25, anchor="nw")  # Positioned under version selector

def browse_directory():
    initial_dir = current_dir.get() if is_valid_minecraft_dir(current_dir.get()) else None
    path = filedialog.askdirectory(
        title="Select Minecraft Folder",
        initialdir=initial_dir
    )
    
    if path:
        if is_valid_minecraft_dir(path):
            current_dir.set(path)
            save_config(path)  # Remember valid path
            messagebox.showinfo("Success", "Valid Minecraft folder selected!")
        else:
            messagebox.showerror(
                "Invalid Folder",
                "This doesn't appear to be a Minecraft installation folder.\n"
                "Please select a folder containing:\n"
                "- /mods (Forge/Fabric)\n"
                "- /versions (Vanilla)\n"
                "- /resourcepacks"
            )

# UI Elements for Directory Browser
ctk.CTkLabel(dir_frame, text="Installation Folder:").pack(anchor="w")
ctk.CTkLabel(
    dir_frame,
    textvariable=current_dir,
    wraplength=280,
    justify="left"
).pack(anchor="w", pady=(0, 5))

ctk.CTkButton(
    dir_frame,
    text="Browse Folder",
    command=browse_directory
).pack(fill="x")

# --- Update/Play Button ---
button_frame = ctk.CTkFrame(app)
button_frame.place(relx=0.5, rely=0.9, anchor="center")
progress_bar = ctk.CTkProgressBar(button_frame, width=300)
progress_bar.pack(pady=5)

def launch_game():
    if not is_valid_minecraft_dir(current_dir.get()):
        messagebox.showwarning(
            "Invalid Folder",
            "Please select a valid Minecraft folder first!"
        )
        return browse_directory()  # Auto-open folder dialog
    
    print(f"Launching from: {current_dir.get()}")

action_button = ctk.CTkButton(button_frame, text="Play", width=200, command=launch_game)
action_button.pack(pady=5)

app.mainloop()