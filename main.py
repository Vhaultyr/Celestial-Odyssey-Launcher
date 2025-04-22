import customtkinter as ctk
from PIL import Image
import requests

# === Launcher Widgets ===
class Widgets:
    def __init__(self, app):
        self.app = app
        self.setup_widgets()


    def setup_widgets(self):
        # TITLE LABEL
        title_label = ctk.CTkLabel(self.app, text="Welcome to Celestial Odyssey Launcher", font=("Arial", 20))
        title_label.place(relx=0.5, rely=0.1, anchor="center")

        # NEWS PANEL
        try:
            response = requests.get("https://raw.githubusercontent.com/Vhaultyr/Celestial-Odyssey-Launcher/main/CHANGELOG.md")
            if response.status_code == 200:
                changelog_content = response.text
            else:
                changelog_content = "Failed to fetch CHANGELOG.md from GitHub."
        except requests.RequestException as e:
            changelog_content = f"Error fetching CHANGELOG.md: {e}"

        news_textbox = ctk.CTkTextbox(self.app, width=600, height=300)
        news_textbox.insert("1.0", changelog_content)
        news_textbox.place(relx=0.5, rely=0.5, anchor="center")
        news_textbox.configure(state="disabled")  # Make it read-only

        # LAUNCH BUTTON
        launch_button = ctk.CTkButton(self.app, text="Launch Game", command=self.launch_game)
        launch_button.place(relx=0.5, rely=0.8, anchor="center")


    def launch_game(self):
        print("Launching the game...")  # Replace with actual game launch logic

# === Main Application Class ===
class CelestialOdysseyLauncher:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Celestial Odyssey Launcher")
        self.app.geometry("1024x576")
        self.app.resizable(width=False, height=False)
        self.app.iconbitmap("assets/icon.ico")
        self.setup_background()

    def setup_background(self):
        # Set the background image
        bg_image = ctk.CTkImage(Image.open("assets/bg.png"), size=(1024, 576))
        bg_label = ctk.CTkLabel(self.app, image=bg_image, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Initialize the UI
        self.ui = Widgets(self.app)

    def run(self):
        self.app.mainloop()

# === Run the Application ===
if __name__ == "__main__":
    launcher = CelestialOdysseyLauncher()
    launcher.run()