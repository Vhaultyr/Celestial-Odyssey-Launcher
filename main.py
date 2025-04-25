import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGroupBox, QVBoxLayout, QWidget, QPushButton, QLayout
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea
import requests

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

        # === UI Widgets ===
        self.news_box()
        self.game_buttons()

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

        # === DEBUG TOOL ===

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
        news.setGeometry(60, 130, 620, 420)

        scroll_area = QScrollArea(news)
        scroll_area.setGeometry(5, 40, 605, 365)
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

    def game_buttons(self):
        # Create a container widget for the buttons
        button_container = QWidget(self)
        button_container.setGeometry(900, 200, 300, 350)  # Positioned on the right side
        button_container.setStyleSheet("background: transparent;")  # Transparent background

        # Create a vertical layout for the buttons
        layout = QVBoxLayout(button_container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align buttons to the top
        layout.setSpacing(30)  # Space between buttons

        # Create the buttons
        mods_button = QPushButton("Mods", button_container)
        packs_button = QPushButton("Packs", button_container)
        about_button = QPushButton("About Us", button_container)
        update_play_button = QPushButton("Play", button_container)
    
        # Set button styles
        for button in [mods_button, packs_button, about_button]:
            button.setStyleSheet("""
                QPushButton {
                background-color: #c5405f;
                font: bold;
                color: #F5F5DC;
                font-family: 'Blockblueprint';
                border: #060034;
                font-size: 40px;
                }
                QPushButton:hover {
                    background-color: #F5F5DC;
                    color: #2E2E2E;
                }
            """)
        for button in [update_play_button]:
            button.setStyleSheet("""
                QPushButton {
                background-color: #c5405f;
                font: bold;
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
            # First 3 buttons are the same size
            layout.addWidget(mods_button)
            layout.addWidget(packs_button)
            layout.addWidget(about_button)

            # Spacer
            layout.addSpacing(60)

            # Last button
            layout.addWidget(update_play_button)
    
        # Example: Connect buttons to actions
        mods_button.clicked.connect(lambda: print("Mods Button clicked"))
        packs_button.clicked.connect(lambda: print("Packs Button clicked"))
        about_button.clicked.connect(lambda: print("About Us clicked"))
        update_play_button.clicked.connect(lambda: print("Update/Play clicked"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())