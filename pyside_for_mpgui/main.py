import sys
from PySide6.QtWidgets import QApplication
from module import MainWindow

def main():
    # Create the application object
    app = QApplication(sys.argv)
    app.setStyleSheet("""
            QToolTip {
                background-color: lightblue;
                color: black;
                border: 1px solid #999999;
            }
        """)
    # Create and show the main window
    window = MainWindow()
    window.show()

    # Run the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
