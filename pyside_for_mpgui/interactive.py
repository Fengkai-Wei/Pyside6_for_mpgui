import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt

class GridWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QGridLayout
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Add some widgets to the grid layout
        self.add_custom_label('Cell 1', 0, 0)
        self.add_custom_label('Cell 2', 0, 1)
        self.add_custom_label('Cell 3', 1, 0)
        self.add_custom_label('Cell 4', 1, 1)

        # Minimize the spacing between widgets
        self.grid_layout.setSpacing(0)
        
        # Minimize the margins around the layout
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

    def add_custom_label(self, text, row, column):
        label = QLabel(text)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(Qt.AlignCenter)
        # Remove margins for each QLabel
        label.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.addWidget(label, row, column)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Grid Layout Example with Fixed Ratio')
        

        # Create a central widget and set it as the central widget for the main window
        self.central_widget = GridWidget()
        self.setCentralWidget(self.central_widget)

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
