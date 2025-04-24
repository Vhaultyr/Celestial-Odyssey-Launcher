import PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Celestial Odyssey Launcher")
        self.setWindowIcon(PyQt6.QtGui.QIcon("assets/icon.png"))
        self.setGeometry(100, 100, 1024, 576)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()