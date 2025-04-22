import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import configparser
from PIL import Image
import os
import sys
import requests
import configparser

# === Launcher Components ===

class Widgets: # UI ELEMENTS
    def __init__(self, app):
        self.app = app
        self.title()
        self.changelog()

    def title(self):  # TITLE
        title_label = ctk.CTkLabel(self.app, text="Welcome to Celestial Odyssey Launcher", font=("Arial", 20))
        title_label.place(relx=0.5, rely=0.1, anchor="center")

    def changelog(self):  # NEWS PANEL
        try:
            response = requests.get("https://raw.githubusercontent.com/Vhaultyr/Celestial-Odyssey-Launcher/refs/heads/main/CHANGELOG.md")
            if response.status_code == 200:
                changelog_content = response.text
            else:
                changelog_content = "Failed to fetch CHANGELOG.md from GitHub."
        except requests.RequestException as e:
            changelog_content = f"Error fetching CHANGELOG.md: {e}"

        news_textbox = ctk.CTkTextbox(self.app, width=400, height=250, wrap="word")
        news_textbox.insert("1.0", changelog_content)
        news_textbox.place(relx=0.25, rely=0.45, anchor="center")
        news_textbox.configure(state="disabled")  # Make it read-only

class Utils: # UTILITY FUNCTIONS
    def __init__(self, app):
        self.app = app
        self.gameinfo()
        self.launch()

    def gameinfo(self):  # GAME INFO PANEL
    # Create a frame to contain all game info widgets
        gameinfo_frame = ctk.CTkFrame(self.app, width=500, height=400)
        gameinfo_frame.place(relx=0.8, rely=0.5, anchor="center")

        # Panel Title
        panel_label = ctk.CTkLabel(gameinfo_frame, text="Game Settings", font=("Arial", 16))
        panel_label.pack(pady=10)

        # Dropdown for Version Selection
        version_label = ctk.CTkLabel(gameinfo_frame, text="Select Version:")
        version_label.pack(pady=(10, 0))

        self.versions = ["Ultra", "Low"]
        self.selected_version = ctk.StringVar(value="Ultra")
        version_dropdown = ctk.CTkOptionMenu(gameinfo_frame, variable=self.selected_version, values=self.versions, command=self.load_config)
        version_dropdown.pack(pady=5)

        # Folder Selector
        folder_label = ctk.CTkLabel(gameinfo_frame, text="Game Folder:")
        folder_label.pack(pady=(10, 0))

        self.folder_path = ctk.StringVar(value="No folder selected")
        folder_button = ctk.CTkButton(gameinfo_frame, text="Select Folder", command=self.select_folder)
        folder_button.pack(pady=5)

        folder_display = ctk.CTkLabel(gameinfo_frame, textvariable=self.folder_path, wraplength=250)
        folder_display.pack(pady=5)

        # Launcher Shortcut Selector
        shortcut_label = ctk.CTkLabel(gameinfo_frame, text="Launcher Shortcut:")
        shortcut_label.pack(pady=(10, 0))

        self.shortcut_name = ctk.StringVar(value="No shortcut selected")
        shortcut_button = ctk.CTkButton(gameinfo_frame, text="Select Shortcut", command=self.select_shortcut)
        shortcut_button.pack(pady=5)

        shortcut_display = ctk.CTkLabel(gameinfo_frame, textvariable=self.shortcut_name, wraplength=250)
        shortcut_display.pack(pady=5)

        # Load initial configuration
        self.load_config(self.selected_version.get())

    def load_config(self, selected_version):
        config = configparser.ConfigParser()
        config.read("config.ini")
        if selected_version in config:
            version_config = config[selected_version]
            self.folder_path.set(version_config.get("GameFolder", "No folder selected"))
            self.shortcut_name.set(version_config.get("LauncherShortcut", "No shortcut selected"))
            print(f"Loaded configuration for {selected_version}: {version_config}")
        else:
            self.folder_path.set("No folder selected")
            self.shortcut_name.set("No shortcut selected")
            print(f"No configuration found for {selected_version}")

    def select_folder(self):
        folder_selected = fd.askdirectory()
        if folder_selected:
            shortened_path = os.path.relpath(folder_selected, start=os.path.expanduser("~"))
            self.folder_path.set(shortened_path)
            self.save_settings()  # Automatically save settings after selection

    def select_shortcut(self):
        shortcut_selected = fd.askopenfilename(filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")])
        if shortcut_selected:
            shortcut_name = os.path.basename(shortcut_selected)
            self.shortcut_name.set(shortcut_name)
            self.save_settings()  # Automatically save settings after selection

    def save_settings(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        config[self.selected_version.get()] = {
            "GameFolder": self.folder_path.get(),
            "LauncherShortcut": self.shortcut_name.get()
        }
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        print(f"Settings saved for {self.selected_version.get()}")
        config = configparser.ConfigParser()
        config[self.selected_version.get()] = {
            "GameFolder": self.folder_path.get(),
            "LauncherShortcut": self.shortcut_name.get()
        }
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        mb.showinfo("Settings Saved", "Your settings have been saved successfully!")

    def launch(self):  # LAUNCH BUTTON
        launch_button = ctk.CTkButton(self.app, text="Launch Game", command=self.launch)
        launch_button.place(relx=0.5, rely=0.9, anchor="center")

# === Main Application Class ===
class CelestialOdysseyLauncher:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Celestial Odyssey Launcher")
        self.app.geometry("1024x576")
        self.app.resizable(width=False, height=False)
        self.app.iconbitmap("assets/icon.ico")
        self.setup_background()
        self.init()

    def setup_background(self):
        # Set the background image
        bg_image = ctk.CTkImage(Image.open("assets/bg.png"), size=(1024, 576))
        bg_label = ctk.CTkLabel(self.app, image=bg_image, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def init(self):
        # Initialize Components
        self.utils = Utils(self.app)
        self.ui = Widgets(self.app)

    def run(self):
        self.app.mainloop()

# === Run the Application ===
if __name__ == "__main__":
    launcher = CelestialOdysseyLauncher()
    launcher.run()