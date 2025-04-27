import sys
from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGroupBox, QVBoxLayout, QWidget, QPushButton, QProgressBar, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea
import requests
from configparser import ConfigParser

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(100, 100, 1280, 720)
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(1280, 720)
        self.background()

        # === Utils ===
        self.oldPos = None  # For Window Movement
        self.dragMainWindow()
        self.app_settings_button() # Settings Menu + Configuration
        self.system_buttons()
        self.firstLaunch()

        # === UI Widgets ===
        self.news_box()
        self.game_buttons()
        self.version_select()
        self.on_version_selected("Low")  # Default selection
        self.play_or_update()
        self.progress_bar()
        self.socials()

        # === DEBUG TOOL ===
        # Move the preview to the 2nd screen while testing

        self.move_to_second_monitor()

    def move_to_second_monitor(self):
        # Get the list of screens
        screens = QApplication.screens()
        if len(screens) > 1:  # Check if a second monitor exists
            second_screen = screens[1]
            geometry = second_screen.geometry()
            # Move the window to the second monitor
            self.move(geometry.x(), geometry.y())
        else:
            print("Second monitor not detected. Opening on the primary monitor.")

    def background(self):
        bg = QLabel(self)
        bg.setPixmap(QtGui.QPixmap("assets/bg.png"))
        bg.setScaledContents(True)
        bg.setGeometry(0, 0, 1280, 720)

        title = QLabel(self)
        title.setText("Celestial Odyssey")
        title.setStyleSheet("""
        color: #F5F5DC;
        font: bold;
        font: 70px;
        font-family: 'Blockblueprint';
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setGeometry(0, 10, 1280, 100)
        title.setWordWrap(True)

    def system_buttons(self):
        self.minimize_button = QPushButton("-", self)
        self.minimize_button.setGeometry(1200, 10, 30, 30)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #c5405f;
                font: bold;
                color: #F5F5DC;
                font-family: 'Blockblueprint';
                border: #060034;
                font-size: 30px;
            }
            QPushButton:hover {
                background-color: #F5F5DC;
                color: #2E2E2E;
            }
        """)
        self.close_button = QPushButton("X", self)
        self.close_button.setGeometry(1240, 10, 30, 30)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #c5405f;
                font: bold;
                color: #F5F5DC;
                font-family: 'Blockblueprint';
                border: #060034;
                font-size: 30px;
            }
            QPushButton:hover {
                background-color: #F5F5DC;
                color: #2E2E2E;
            }
        """)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.close_button.clicked.connect(self.close)

    def news_box(self):
        news = QGroupBox("News", self)
        news.setStyleSheet("""
            QGroupBox {
            color: #F5F5DC;
            font: bold;
            font-size: 40px;
            font-family: 'Blockblueprint';
            border: 1px solid gray;
            border-radius: 5px;
            margin-top: 20px;
            letter-spacing: 3px;
            }
            QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 10px;
            }
        """)
        news.setGeometry(60, 150, 620, 360)

        scroll_area = QScrollArea(news)
        scroll_area.setGeometry(5, 40, 605, 305)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #2E2E2E;
                width: 14px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #F5F5DC;
                min-height: 20px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }                         
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(scroll_content)
        scroll_label = QLabel(scroll_content)
        try:
            url = "https://raw.githubusercontent.com/Vhaultyr/Celestial-Odyssey-Launcher/refs/heads/main/CHANGELOG.md"
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            changelog_text = response.text
        except requests.exceptions.RequestException as e:
            changelog_text = f"Failed to load changelog: {e}"

        scroll_label.setText(changelog_text)
        scroll_label.setWordWrap(True)
        scroll_label.setStyleSheet("""

        QLabel {
            color: #F5F5DC;
            font-size: 20px;
            font-family: 'Blockblueprint';
            }

        """)

        layout.addWidget(scroll_label)
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)

    def dragMainWindow(self):
        def mousePressEvent(event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.oldPos = event.globalPosition().toPoint()  # Convert to QPoint

        def mouseMoveEvent(event):
            if self.oldPos is not None:
                delta = event.globalPosition().toPoint() - self.oldPos  # Convert to QPoint
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPosition().toPoint()  # Update position

        def mouseReleaseEvent(event):
            self.oldPos = None

        # Assign the event handlers to the window
        self.mousePressEvent = mousePressEvent
        self.mouseMoveEvent = mouseMoveEvent
        self.mouseReleaseEvent = mouseReleaseEvent
        
    def app_settings_button(self):
        self.open_settings = QPushButton("Settings", self)
        self.open_settings.setGeometry(1058, 10, 130, 30)
        self.open_settings.setStyleSheet("""
            QPushButton {
                background-color: #c5405f;
                font: bold;
                color: #F5F5DC;
                font-family: 'Blockblueprint';
                border: #060034;
                font-size: 30px;
            }
            QPushButton:hover {
                background-color: #F5F5DC;
                color: #2E2E2E;
            }
        """)
        self.open_settings.clicked.connect(self.open_settings_menu)

    def open_settings_menu(self):
        self.settings_window = SettingsMenu(parent=self)  # Pass MainWindow as the parent
        self.settings_window.show()

    def game_buttons(self):
        # Create a container widget for the buttons
        button_container = QWidget(self)
        button_container.setGeometry(850, 200, 300, 600)  # Positioned on the right side
        button_container.setStyleSheet("background: transparent;")  # Transparent background

        # Create a vertical layout for the buttons
        layout = QVBoxLayout(button_container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align buttons to the top
        layout.setSpacing(60)  # Space between buttons

        # Create the buttons
        mods_button = QPushButton("Mods", button_container)
        packs_button = QPushButton("Packs", button_container)
        about_button = QPushButton("About Us", button_container)
    
        # Set button styles
        for button in [mods_button, packs_button, about_button]:
            button.setStyleSheet("""
                QPushButton {
                background-color: #c5405f;
                color: #F5F5DC;
                font-family: 'Blockblueprint';
                border: #060034;
                font-size: 50px;
                }
                QPushButton:hover {
                    background-color: #F5F5DC;
                    color: #2E2E2E;
                }
            """)
            # Add Buttons to BoxLayout
            layout.addWidget(mods_button)
            layout.addWidget(packs_button)
            layout.addWidget(about_button)
    
        # Example: Connect buttons to actions
        mods_button.clicked.connect(lambda: print("Mods Button clicked"))
        packs_button.clicked.connect(lambda: print("Packs Button clicked"))
        about_button.clicked.connect(lambda: print("About Us clicked"))

    def play_or_update(self):
        play_button = QPushButton("Play", self)
        play_button.setGeometry(825, 585, 350, 90)
        play_button.setStyleSheet("""
            QPushButton {
                background-color: #c5405f;
                color: #F5F5DC;
                font-family: 'Blockblueprint';
                border: #060034;
                font-size: 70px;
            }
            QPushButton:hover {
                background-color: #F5F5DC;
                color: #2E2E2E;
            }
        """)
        play_button.clicked.connect(lambda: print("Play button clicked"))

    def progress_bar(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(60, 620, 620, 30)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2E2E2E;
                border: 1px solid gray;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #c5405f;
                border-radius: 5px;
            }
        """)

        # Add a label above the progress bar to display the status text
        self.progress_label = QLabel("Initializing...", self)
        self.progress_label.setGeometry(60, 590, 620, 30)  # Positioned above the progress bar
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("""
            QLabel {
                color: #F5F5DC;
                font-size: 20px;
                font-family: 'Blockblueprint';
            }
        """)

    def socials(self):
        socials_container = QWidget(self)
        socials_container.setGeometry(30, 30, 700, 70)
        socials_container.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(socials_container)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setSpacing(20)

        # Create a button with an image
        discord_button = QPushButton(socials_container)
        discord_button.setIcon(QtGui.QIcon("assets/disc_icon.png"))  # Set the image as the button icon
        discord_button.setIconSize(QtCore.QSize(64, 64))  # Adjust the size of the icon
        discord_button.setStyleSheet("""
            QPushButton {
                background: transparent;  /* Remove background */
                border: none;  /* Remove border */
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);  /* Optional hover effect */
            }
        """)
        discord_button.clicked.connect(lambda: print("Discord button clicked"))  # Example action

        # Add the button to the layout
        layout.addWidget(discord_button)

    def version_select(self):
        # Create a QComboBox for version selection
        version_dropdown = QComboBox(self)
        version_dropdown.setGeometry(825, 540, 350, 30)  # Positioned directly above the play/update button
        version_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #2E2E2E;
                color: #F5F5DC;
                border: 1px solid gray;
                border-radius: 5px;
                font-size: 30px;
                font-family: 'Blockblueprint';
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2E2E2E;
                color: #F5F5DC;
                selection-background-color: #c5405f;
                selection-color: #F5F5DC;
            }
        """)

        # Add options to the dropdown with tooltips
        version_dropdown.addItem("Low")
        version_dropdown.setItemData(0, "6 GB RAM Recommended - Optimized for older systems or low-end hardware.", Qt.ItemDataRole.ToolTipRole)
        
        version_dropdown.addItem("Ultra")
        version_dropdown.setItemData(1, "8 GB RAM Recommended - Best visuals, recommended for high-end systems.", Qt.ItemDataRole.ToolTipRole)

        # Connect the dropdown to a function to handle selection changes
        version_dropdown.currentTextChanged.connect(self.on_version_selected)

    def on_version_selected(self, selected_version):
        # Handle the version selection
        if selected_version == "Low":
            print("Low version selected")
            # Add logic for Low version here
        elif selected_version == "Ultra":
            print("Ultra version selected")
            # Add logic for Ultra version here

    def firstLaunch(self):
        # Check if it's the first launch by reading the config.ini file

        config = ConfigParser()
        config_file = "config.ini"

        # Check if the config file exists
        try:
            config.read(config_file)
            first_launch = config.getboolean("Settings", "FirstLaunch", fallback=True)
        except Exception as e:
            print(f"Error reading config file: {e}")
            first_launch = True

        if first_launch:
            print("First launch detected.")
            # Update the config file to mark first launch as False
            if not config.has_section("Settings"):
                config.add_section("Settings")
            config.set("Settings", "FirstLaunch", "False")
            with open(config_file, "w") as file:
                config.write(file)

class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0, 0, 400, 300)
        self.setStyleSheet("background-color: #2E2E2E; color: #F5F5DC; border: 1px solid gray;")
        self.center_on_parent(parent)
        self.dragSettingsMenu()

    def center_on_parent(self, parent):
        if parent:
            # Ensure the size of the SettingsMenu is set before calculating its position
            self.resize(400, 300)  # Explicitly set the size of the SettingsMenu

            parent_geometry = parent.geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)

    def dragSettingsMenu(self):
        self.oldPos = None

        def mousePressEvent(event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.oldPos = event.globalPosition().toPoint()  # Convert to QPoint
            super(SettingsMenu, self).mousePressEvent(event)

        def mouseMoveEvent(event):
            if self.oldPos is not None:
                delta = event.globalPosition().toPoint() - self.oldPos  # Convert to QPoint
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPosition().toPoint()  # Update position
            super(SettingsMenu, self).mouseMoveEvent(event)

        def mouseReleaseEvent(event):
            self.oldPos = None
            super(SettingsMenu, self).mouseReleaseEvent(event)

        # Bind the event handlers to the SettingsMenu instance
        self.mousePressEvent = mousePressEvent
        self.mouseMoveEvent = mouseMoveEvent
        self.mouseReleaseEvent = mouseReleaseEvent

        # Create a vertical layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)

        # Add a title label
        title_label = QLabel("Settings", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-family: 'Blockblueprint';
                font-weight: bold;
            }
        """)
        layout.addWidget(title_label)

        # Add example settings options
        option1 = QLabel("Option 1: Placeholder", self)
        option2 = QLabel("Option 2: Placeholder", self)
        option3 = QLabel("Option 3: Placeholder", self)

        for option in [option1, option2, option3]:
            option.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-family: 'Blockblueprint';
                }
            """)
            layout.addWidget(option)

        # Add a close button
        close_button = QPushButton("Close", self)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #c5405f;
                color: #F5F5DC;
                font-family: 'Blockblueprint';
                font-size: 18px;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #F5F5DC;
                color: #2E2E2E;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())