import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGroupBox, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Celestial Odyssey Launcher")
        self.setWindowIcon(QtGui.QIcon("assets/icon.ico"))
        self.setGeometry(100, 100, 1280, 720)
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(1280, 720)
        self.background()
        self.ui()

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
        title.setStyleSheet("" \
        "color: #F5F5DC; " \
        "font: 70px;"
        "font-family: 'Blockblueprint';" \
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setGeometry(0, 10, 1280, 100)
        title.setWordWrap(True)

    def ui(self):
        news = QGroupBox("News", self)
        news.setStyleSheet("""
            QGroupBox {
            color: #F5F5DC;
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
        news.setGeometry(60, 130, 320, 500)

        # Create a scrollable text box

        scroll_area = QScrollArea(news)
        scroll_area.setGeometry(10, 40, 300, 450)  # Adjust size to fit inside the GroupBox
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        scroll_label = QLabel(scroll_content)
        scroll_label.setText("This is a scrollable text box.\n" * 80)  # Example long text
        scroll_label.setWordWrap(True)

        layout.addWidget(scroll_label)
        scroll_content.setLayout(layout)

        scroll_area.setWidget(scroll_content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())