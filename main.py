import customtkinter as ctk
import tkinter.filedialog as filedialog
import configparser
from tkinter import messagebox
from PIL import Image
import os

# Initialize the app
app = ctk.CTk()
app.title("Celestial Odyssey Launcher")
app.geometry("1024x576")
app.resizable(width=False, height=False)

# --- Config File Setup ---
config = configparser.ConfigParser()
config_file = "launcher_config.ini"


# Saves last valid path that was selected & uses it the next time app is launched.
def load_config():
    if os.path.exists(config_file):
        config.read(config_file)
        return config.get('Settings', 'LastValidPath', fallback="")
    return ""

def save_config(path):
    config['Settings'] = {'LastValidPath': path}
    with open(config_file, 'w') as f:
        config.write(f)

# Saves the shortcut that was selected & uses it the next time app is launched.
def load_launcher_path():
    config.read(config_file)
    return config.get('Settings', 'LauncherPath', fallback="")

def save_launcher_path(path):
    config['Settings']['LauncherPath'] = path
    with open(config_file, 'w') as f:
        config.write(f)

# --- Validation ---
def is_valid_minecraft_dir(path):
    """Check for mods folder"""
    if not path:
        return False
    return os.path.isdir(os.path.join(path, "mods"))

# --- Load Assets ---
def load_image(path, size):
    try:
        img = Image.open(path)
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
    app.configure(fg_color="#2b2b2b")

# Icon
if os.path.exists("assets/icon.ico"):
    app.iconbitmap("assets/icon.ico")

# --- News Panel ---
news_frame = ctk.CTkFrame(app, width=350, height=400, corner_radius=10)
news_frame.place(relx=0.05, rely=0.1, anchor="nw")

news_label = ctk.CTkLabel(news_frame, text="Latest News", font=ctk.CTkFont(size=16, weight="bold"))
news_label.pack(pady=(10, 5))

news_text = ctk.CTkTextbox(news_frame, width=330, height=350, wrap="word")
news_text.pack(padx=10, pady=(0, 10))
news_text.insert("1.0", "• Launcher initialized\n• Select your modpack folder")
news_text.configure(state="disabled")

# --- Version Selector ---
version_frame = ctk.CTkFrame(app, width=300, corner_radius=10)
version_frame.place(relx=0.7, rely=0.1, anchor="nw")

version_label = ctk.CTkLabel(version_frame, text="Select Version", font=ctk.CTkFont(size=16))
version_label.pack(pady=5)

version_var = ctk.StringVar(value="Ultra")
version_menu = ctk.CTkOptionMenu(version_frame, values=["Ultra", "Low"], variable=version_var)
version_menu.pack(pady=10)

# --- Directory Browser ---
current_dir = ctk.StringVar(value=load_config() or "No folder selected")

dir_frame = ctk.CTkFrame(version_frame)
dir_frame.pack(pady=(20, 0), fill="x", padx=5)

def browse_directory():
    initial_dir = current_dir.get() if is_valid_minecraft_dir(current_dir.get()) else None
    path = filedialog.askdirectory(title="Select Modpack Folder", initialdir=initial_dir)
    
    if path:
        if is_valid_minecraft_dir(path):
            current_dir.set(path)
            save_config(path)
        else:
            messagebox.showerror("Invalid Folder", "Please select a folder containing a /mods directory")

ctk.CTkLabel(dir_frame, text="Modpack Folder:").pack(anchor="w")
dir_label = ctk.CTkLabel(dir_frame, textvariable=current_dir, wraplength=280, justify="left")
dir_label.pack(anchor="w", pady=(0, 5))

browse_button = ctk.CTkButton(dir_frame, text="Browse", width=80, command=browse_directory)
browse_button.pack(pady=5)

# Shortcut Selector

launcher_path_var = ctk.StringVar(value=load_launcher_path() or "No launcher selected")

def browse_launcher_shortcut():
    path = filedialog.askopenfilename(
        title="Select Launcher Shortcut",
        filetypes=[("Shortcut, EXE, or Script", "*.lnk *.exe *.bat *.cmd")],
    )
    if path:
        launcher_path_var.set(path)
        save_launcher_path(path)

ctk.CTkLabel(dir_frame, text="Launcher Shortcut:").pack(anchor="w")
launcher_label = ctk.CTkLabel(dir_frame, textvariable=launcher_path_var, wraplength=280, justify="left")
launcher_label.pack(anchor="w", pady=(0, 5))

launcher_button = ctk.CTkButton(dir_frame, text="Select Launcher", width=80, command=browse_launcher_shortcut)
launcher_button.pack(pady=5)


# --- Update/Play Button ---
button_frame = ctk.CTkFrame(app)
button_frame.place(relx=0.5, rely=0.9, anchor="center")

progress_bar = ctk.CTkProgressBar(button_frame, width=300)
progress_bar.pack(pady=5)
progress_bar.set(0)

def is_up_to_date():
    """Placeholder - replace with real version check"""
    return True

def update_modpack():
    """Placeholder update function"""
    progress_bar.start()
    app.after(2000, lambda: [
        progress_bar.stop(),
        messagebox.showinfo("Success", "Modpack updated successfully!"),
        action_button.configure(text="Play")
    ])

def launch_game():
    launcher_path = launcher_path_var.get()
    if not os.path.exists(launcher_path):
        messagebox.showerror("Error", "Please select a valid launcher shortcut or executable")
        return
    try:
        os.startfile(launcher_path)
    except Exception as e:
        messagebox.showerror("Launch Error", f"Could not launch the shortcut:\n{e}")


action_button = ctk.CTkButton(
    button_frame,
    text="Play" if is_up_to_date() else "Update",
    width=200,
    command=lambda: launch_game() if is_up_to_date() else update_modpack()
)
action_button.pack(pady=5)

app.mainloop()