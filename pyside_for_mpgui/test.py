import sys


from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QMenu, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QSlider, QDoubleSpinBox, QTabWidget, QGridLayout)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class CustomEditDialog(QDialog):
    def __init__(self, item_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Item")
        self.setGeometry(100, 100, 300, 200)

        # Store the item text
        self.item_text = item_text

        # Create layout
        layout = QFormLayout(self)

        # Create a text input
        self.text_input = QLineEdit()
        self.text_input.setText(self.item_text)
        layout.addRow("Text:", self.text_input)
        self.text_input.textChanged.connect(self.on_text_changed)

        # Create a float input
        self.float_input = QDoubleSpinBox()
        self.float_input.setRange(0, 100)
        self.float_input.setSingleStep(0.1)
        layout.addRow("Float Input:", self.float_input)
        self.float_input.valueChanged.connect(self.on_float_input_changed)

        # Create a float slider
        self.float_slider = QSlider(Qt.Horizontal)
        self.float_slider.setRange(0, 100)
        self.float_slider.setSingleStep(1)
        layout.addRow("Float Slider:", self.float_slider)
        self.float_slider.valueChanged.connect(self.on_float_slider_changed)

        # Create a combo box
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        layout.addRow("Combo Box:", self.combo_box)
        self.combo_box.currentTextChanged.connect(self.on_combo_box_changed)

        # Create buttons
        self.button_box = QPushButton("OK")
        self.button_box.clicked.connect(self.accept)
        layout.addRow(self.button_box)

        self.setLayout(layout)

    def get_values(self):
        return {
            "text": self.text_input.text(),
            "float_input": self.float_input.value(),
            "float_slider": self.float_slider.value(),
            "combo_box": self.combo_box.currentText()
        }

    def on_text_changed(self, new_text):
        print(f"Text input changed: {new_text}")

    def on_float_input_changed(self, new_value):
        print(f"Float input changed: {new_value}")

    def on_float_slider_changed(self, new_value):
        print(f"Float slider changed: {new_value}")

    def on_combo_box_changed(self, new_text):
        print(f"Combo box changed: {new_text}")

class CustomListWidget(QWidget):
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        if items is None:
            items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        self.list_items = items
        self.init_ui()

    def init_ui(self):
        # Create and configure the list widget
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.list_items)
        self.list_widget.setDragEnabled(True)  # Enable drag operations
        self.list_widget.setDropIndicatorShown(True)  # Show drop indicator
        self.list_widget.setDragDropMode(QListWidget.InternalMove)  # Allow internal moves

        # Set context menu policy and connect the signal
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        # Create and configure the add button
        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item)

        # Layout configuration
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.add_button)

        # Connect the signals for drag-and-drop operations
        self.list_widget.model().rowsMoved.connect(self.print_list_items)
        self.list_widget.model().rowsRemoved.connect(self.print_list_items)
        self.list_widget.model().rowsInserted.connect(self.print_list_items)

    def add_item(self, item_text=None):
        # Add a new item to the list
        if not item_text:
            item_text = f"Item {self.list_widget.count() + 1}"
        self.list_widget.addItem(item_text)
        self.print_list_items()

    def show_context_menu(self, pos):
        # Create and show the context menu
        menu = QMenu(self)
        
        edit_action = QAction("Edit", self)
        delete_action = QAction("Delete", self)
        copy_action = QAction("Copy", self)

        menu.addAction(edit_action)
        menu.addAction(delete_action)
        menu.addAction(copy_action)

        # Connect actions to methods
        edit_action.triggered.connect(self.edit_item)
        delete_action.triggered.connect(self.delete_item)
        copy_action.triggered.connect(self.copy_item)

        # Get the item that was right-clicked
        index = self.list_widget.indexAt(pos)
        if index.isValid():
            self.current_item = self.list_widget.itemFromIndex(index)
            menu.exec(self.list_widget.mapToGlobal(pos))

    def edit_item(self):
        # Show a popup with various input fields
        if hasattr(self, 'current_item'):
            dialog = CustomEditDialog(self.current_item.text(), self)
            if dialog.exec():
                values = dialog.get_values()
                print(f"Edited values: {values}")
                self.current_item.setText(values['text'])

    def delete_item(self):
        # Permanently delete the item
        if hasattr(self, 'current_item'):
            row = self.list_widget.row(self.current_item)
            self.list_widget.takeItem(row)
            self.print_list_items()

    def copy_item(self):
        # Copy the item text to the end of the list
        if hasattr(self, 'current_item'):
            new_item_text = f"{self.current_item.text()} (Copy)"
            self.add_item(new_item_text)
            self.print_list_items()

    def print_list_items(self):
        # Print all items in the list
        print("Current list items:")
        for index in range(self.list_widget.count()):
            print(self.list_widget.item(index).text())

class CustomButton(QWidget):
    def __init__(self, label="Add", parent=None):
        super().__init__(parent)
        self.button_label = label
        self.init_ui()

    def init_ui(self):
        # Create and configure the button
        self.button = QPushButton(self.button_label)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.show_popup)

    def show_popup(self):
        # Create and show a message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Popup")
        msg_box.setText("This is a popup message.")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a matplotlib figure and axis
        self.figure, self.ax = plt.subplots()

        # Create a FigureCanvas object
        self.canvas = FigureCanvas(self.figure)

        # Create a QVBoxLayout for this widget
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)  # Set the layout for this widget

        # Add the canvas to the layout
        self.layout.addWidget(self.canvas)

        # Plot some example data
        self.plot()

    def plot(self, scale=1):
        # Clear previous plot
        self.ax.clear()

        # Example plot with dynamic scaling
        x = [1, 2, 3, 4]
        y = [1, 4, 9, 16]
        self.ax.plot(x, [i * scale for i in y], 'r-')
        self.ax.set_xlabel('X Axis')
        self.ax.set_ylabel('Y Axis')
        self.ax.set_title('Interactive Plot')

        # Draw the plot
        self.canvas.draw()

class SliderWidget(QWidget):
    def __init__(self, plot_widget, parent=None):
        super().__init__(parent)
        self.plot_widget = plot_widget

        # Create a slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        
        # Connect the slider value change event to a method
        self.slider.valueChanged.connect(self.update_plot)

        # Create a QVBoxLayout for this widget
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Add the slider to the layout
        self.layout.addWidget(self.slider)

    def update_plot(self):
        # Update the plot based on the slider value
        scale = self.slider.value()
        self.plot_widget.plot(scale=scale)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Application")
        self.setGeometry(100, 100, 800, 600)  # Adjust window size for layout

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create and configure layouts
        self.central_layout = QVBoxLayout(central_widget)
        self.tab_widget = QTabWidget()

        # Create and add tabs
        self.tab1 = CustomListWidget()
        self.tab2 = CustomListWidget()
        self.tab3 = CustomListWidget()

        self.tab_widget.addTab(self.tab1, "Tab 1")
        self.tab_widget.addTab(self.tab2, "Tab 2")
        self.tab_widget.addTab(self.tab3, "Tab 3")

        # Create and add the canvas grid widget
        self.plot_widget = PlotWidget()

        # Add the tab widget and canvas grid to the central layout
        self.central_layout.addWidget(self.tab_widget)
        self.central_layout.addWidget(self.plot_widget)

        # Create and add the slider widget
        self.slider_widget = SliderWidget(self.plot_widget)
        self.central_layout.addWidget(self.slider_widget)

        # Create and add widgets
        self.create_label()
        self.button_widget = CustomButton()  # Uses default label "Add"
        self.central_layout.addWidget(self.button_widget)

    def create_label(self):
        # Create a label and set its text
        label = QLabel("This is a GUI for meep")
        self.central_layout.addWidget(label)  # Add the label to the central layout

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
