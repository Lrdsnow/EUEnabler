from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EUEnabler")
        self.setFixedSize(960, 540)
        self.setWindowIcon(QIcon("icon.png"))
        self.center()

    def center(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()

        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        self.move(x, y)