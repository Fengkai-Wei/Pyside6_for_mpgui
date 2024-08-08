import sys
from PySide6.QtWidgets import QApplication
from module import *

def main():
    # Create the application object
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Run the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
