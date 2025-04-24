from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Celestial Odyssey Launcher")
        self.setWindowIcon(QtGui.QIcon("assets/icon.png"))
        self.setGeometry(100, 100, 1024, 576)

        # Set a central widget (needed for layouts)
        central_widget = QLabel(self)
        self.setCentralWidget(central_widget)

        # Apply stylesheet for the background (scales with window)
        self.setStyleSheet("""
            QMainWindow {
                background-image: url(assets/background.png);
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
            }
        """)

        # Add a title label (centered at the top)
        title = QLabel("Celestial Odyssey", self)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                margin-top: 40px;
            }
        """)

if __name__ == "__main__":
    import sys
    from PyQt6 import QtGui  # Import QtGui for QIcon

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())