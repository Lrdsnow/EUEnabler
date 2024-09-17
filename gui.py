from backend.device_manager import DeviceManager
from backend.mainwindow import MainWindow
from PySide6.QtWidgets import QApplication
import sys
from tweak.eligibility import EUTweak

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dev_manager = DeviceManager()
    tweak = EUTweak()

    window = MainWindow(dev_manager, tweak)
    window.show()

    sys.exit(app.exec())