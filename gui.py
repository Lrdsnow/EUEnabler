from backend.mainwindow import MainWindow
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Run the application's event loop
    sys.exit(app.exec())