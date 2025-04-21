import customtkinter as ctk
import tkinter as tk
from PIL import Image

# === MAIN APP WINDOW ===
class CelestialOdysseyLauncher:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Celestial Odyssey Launcher")
        self.app.geometry("1024x576")
        self.app.resizable(width=False, height=False)
        self.app.iconbitmap("assets/icon.ico")
        
        # Background Image
        bg_image = ctk.CTkImage(Image.open("assets/bg.png"), size=(1024, 576))
        bg_label = ctk.CTkLabel(self.app, image=bg_image, text="")
        bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def run(self):
        self.app.mainloop()

# Create and run the application
if __name__ == "__main__":
    launcher = CelestialOdysseyLauncher()
    launcher.run()