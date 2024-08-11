import sys
import numpy as np
import meep as mp

from PySide6.QtWidgets import (QSizePolicy, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QMenu, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QSlider, QDoubleSpinBox, QTabWidget, QGridLayout)
from PySide6.QtGui import QAction, QFontMetrics
from PySide6.QtCore import Qt
import copy
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
mpl.rcParams['savefig.pad_inches'] = 0

from vispy import scene
from vispy.scene import visuals

import global_vars
from var_manage import add_var, rm_var
global_vars.init()
from  global_vars import var_dict


def reverse_dict(from_dict, find_val):
    key = next((k for k, v in from_dict.items() if v == find_val), None)
    return key

class CustomMsgBox(QMessageBox):
    def __init__(self, parent = None):
        self.parent = parent
    
    def show_msg(self,title, message, icon=QMessageBox.Information,buttons=QMessageBox.Ok):
        # Create the message box and set its parent
        msg_box = QMessageBox(self.parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setStandardButtons(buttons)
        msg_box.exec()  # Show the message box modally

class AddItemDialog(QDialog):
    def __init__(self, type ,combo_list,parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(100, 100, 300, 100)
        self.combo_list = combo_list
        self.type = type
        self.setWindowTitle(f'Add {self.type}')

        # Create layout
        layout = QFormLayout(self)

        # Create input for name of new item
        self.name_input = QLineEdit()
        self.name_input.setText(f'New {self.type}')
        layout.addRow('Name:', self.name_input)
        self.name_input.textChanged.connect(self.on_name_changed)

        # Create combo box for item type
        self.type_combo = QComboBox()
        self.type_combo.addItems(self.combo_list)
        self.type_combo.setMaxVisibleItems(15)
        self.type_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")

        layout.addRow(f'{self.type}:',self.type_combo)
        
        self.type_combo.currentTextChanged.connect(self.on_combo_box_changed)



        # Create buttons
        self.button_box = QPushButton("OK")
        self.button_box.clicked.connect(self.check_name)
        layout.addRow(self.button_box)

        self.setLayout(layout)
    def check_name(self):
        if self.name_input.text() in self.parent.print_list_items():
            self.msg =  CustomMsgBox(self)
            self.msg.show_msg(
                title = 'Invalid Name',
                message = f"{self.name_input.text()} is already named",
                icon = QMessageBox.Warning,
                buttons = QMessageBox.Ok
            )
        else:
            super().accept()
        



    def on_name_changed(self,new_name):
        print(f"Name input changed: {new_name}")
    def on_combo_box_changed(self, new_text):
        print(f"Name input changed: {new_text}")
    def get_values(self):
        return {'name':self.name_input.text(),
                'type':self.type_combo.currentText()}




class CustomEditDialog(QDialog):
    def __init__(self, item_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Item")
        self.setGeometry(100, 100, 300, 200)

        # Check which dict should be edited
        self.edit_class = parent.add_type
        # Create layout
        layout = QFormLayout(self)

        if self.edit_class == 'Structure':

            self.target_dict = var_dict['geo']

        elif self.edit_class == 'Sources':

            self.target_dict = var_dict['src']

        elif self.edit_class == 'Monitors':

            self.target_dict = var_dict['dft']

        # Store the item text
        self.item_text = item_text

        

        # Get all attr of object
        parent.print_list_items()
        print(self.target_dict[self.item_text].__dict__)
        attr_list = self.target_dict[self.item_text].__dict__
        def input_select(value):


            if isinstance(value, float):
                temp_widget = QDoubleSpinBox()
                temp_widget.setFixedHeight(30)
                temp_widget.setValue(value)
                return temp_widget
            
            elif isinstance(value, mp.Vector3):
                temp_widget = QWidget()
                temp_layout = QHBoxLayout(temp_widget)
                for i in value:
                    spin_box = QDoubleSpinBox()
                    spin_box.setValue(i)
                    spin_box.setFixedHeight(30)
                    temp_layout.addWidget(spin_box)
                return temp_widget
            
            elif isinstance(value, mp.Medium):
                temp_widget = QComboBox()
                
                temp_widget.addItems(list(var_dict['Material'].keys()))
                material_key = reverse_dict(from_dict=var_dict['Material'], find_val=value)
                if material_key == None:
                    material_key = 'Vaccum'
                temp_widget.setCurrentText(material_key)
                temp_widget.setMaxVisibleItems(15)
                temp_widget.setStyleSheet("QComboBox { combobox-popup: 0; }")
                temp_widget.setFixedHeight(30)
                return temp_widget
            
        for (key,value) in attr_list.items():
            # print(key,value)

            key_input = input_select(value=value)
            if key[0] == '_':
                key = key[1:]
            
            layout.addRow(key,key_input)
            pass


       
        



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
    def __init__(self, add_type = 'Structure', add_combo=var_dict['Structure'] ,items=None, parent=None):
        super().__init__(parent)
        if items is None:
            items = []
        self.list_items = items
        self.add_combo = add_combo
        self.add_type = add_type
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
        self.add_button = QPushButton(f"Add {self.add_type}")
        self.add_button.clicked.connect(self.add_item)

        # Layout configuration
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.add_button)

        # Connect the signals for drag-and-drop operations
        self.list_widget.model().rowsMoved.connect(self.print_list_items)
        self.list_widget.model().rowsRemoved.connect(self.print_list_items)
        self.list_widget.model().rowsInserted.connect(self.print_list_items)

    def add_item(self):
        dialog = AddItemDialog(type = self.add_type, combo_list = self.add_combo.keys(),parent = self)
        if dialog.exec():
            values = dialog.get_values()
            print(f"Edited values: {values}")

            # Add a new item to the list
            self.list_widget.addItem(values['name'])

            

            # Add corresponding objects to temp dict for later use
            
            if self.add_type == 'Structure':

                # if add Structure, then add a geometric object
                temp_obj = copy.deepcopy(var_dict['Structure'][values['type']])
                var_dict['geo'].update({values['name']:temp_obj})

            elif self.add_type == 'Sources':

                # if add Sources, then add a geometric object
                temp_obj = var_dict['Sources'][values['type']]
                if temp_obj == mp.source.CustomSource:
                    temp_srct = temp_obj(src_func= lambda t: np.random.randn())
                else:
                    temp_srct = temp_obj(frequency = 1/1.55)
                temp_src = mp.Source(src = temp_srct,component=mp.Ex,center=mp.Vector3(0,0,0))
                var_dict['src'].update({values['name']:temp_src})

            elif self.add_type == 'Monitors':
                pass
                #



        


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
                if self.current_item.text() == values['text']:
                    pass
                else:
                    # Get current list of item
                    current_list = self.print_list_items()

                    # Check if duplicate
                    if values['text'] in current_list:

                        self.msg =  CustomMsgBox(self)
                        self.msg.show_msg(
                            title = 'Invalid Name',
                            message = f"{values['text']} is already named",
                            icon = QMessageBox.Warning,
                            buttons = QMessageBox.Ok
                        )
                        
                    else:
                        self.current_item.setText(values['text'])

    def delete_item(self):
        # Permanently delete the item
        if hasattr(self, 'current_item'):
            row = self.list_widget.row(self.current_item)
            item = self.list_widget.item(row).text()
            self.list_widget.takeItem(row)
            
            if self.add_type == 'Structure':

                var_dict['geo'].pop(item)
                print(f'Geometry: {var_dict["geo"]}')

            elif self.add_type == 'Sources':

                var_dict['src'].pop(item)
                print(f'Sources: {var_dict["src"]}')
            
            elif self.add_type == 'Monitors':
                pass

            self.print_list_items()

    def copy_item(self):
        # Copy the item text to the end of the list
        if hasattr(self, 'current_item'):
            new_item_text = f"{self.current_item.text()} (Copy)"

            self.add_item(new_item_text)
            self.print_list_items()

    def print_list_items(self):
        # Print all items in the list
        list_items = []
        print("Current list items:")
        for index in range(self.list_widget.count()):
            list_items.append(self.list_widget.item(index).text())
        print(list_items)
        return list_items



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

        # Ensure a tight layout
        self.figure.tight_layout()

        # Create a FigureCanvas object
        self.canvas = FigureCanvas(self.figure)

        # Create a QVBoxLayout for this widget
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)  # Set the layout for this widget

        # Add the canvas to the layout
        self.layout.addWidget(self.canvas)


        # Plot some example data
        #self.plot()

        # Remove all paddings
        self.figure.subplots_adjust(top=1,
                            bottom=0,
                            left=0,
                            right=1)

    def plot(self, scale=1):
        # Clear previous plot
        self.ax.clear()
        self.ax.grid(color=(0,0,0,0.1), linestyle='--')
        # Example plot with dynamic scaling
        x = [1, 2, 3, 4]
        y = [1, 4, 9, 16]
        self.ax.plot(x, [i * scale for i in y], 'r-')
        # self.ax.set_xlabel('X Axis')
        # self.ax.set_ylabel('Y Axis')
        self.ax.set_xlim([-6, 6])
        self.ax.set_xticks(np.arange(-6, 6, 1))
        self.ax.set_ylim([-16*scale, 16*scale])
        self.ax.set_yticks(np.arange(-16*scale, 16*scale, 16))


        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')

        # Eliminate upper and right axes
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')

        # Show ticks in the left and lower axes only
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')


        # self.ax.set_title('Interactive Plot')

        # Hide x-axis
        # self.ax.get_xaxis().set_visible(False)

        # Hide y-axis 
        # self.ax.get_yaxis().set_visible(False)

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

class VispyPlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a canvas
        self.canvas = scene.SceneCanvas(keys='interactive', show=True)
        
        # Create a view
        self.view = self.canvas.central_widget.add_view()
        
        # Create 3D axis
        self.view.camera = 'turntable'
        axis = visuals.XYZAxis(parent=self.view.scene)
        
        # Add data
        # self.plot()

        # Create a QVBoxLayout for this widget
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        
        # Add the canvas to the layout
        self.layout.addWidget(self.canvas.native)

    def plot(self):
        # Create some example data
        import numpy as np
        data = np.random.normal(size=(100, 3), scale=0.2)
        
        # Create scatter plot
        scatter = visuals.Markers()
        scatter.set_data(data, edge_color=None, face_color=(1, 1, 1, 0.5), size=5)
        
        # Add scatter plot to the view
        self.view.add(scatter)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Application")
        self.setGeometry(200, 200, 800, 600)  # Adjust window size for layout

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create and configure layouts
        self.central_layout = QVBoxLayout(central_widget)
        self.tab_widget = QTabWidget()

        # Create and add tabs
        self.tab1 = CustomListWidget()
        self.tab2 = CustomListWidget(add_type= 'Sources', add_combo= var_dict['Sources'])
        self.tab3 = CustomListWidget()

        self.tab_widget.addTab(self.tab1, "Tab 1")
        self.tab_widget.addTab(self.tab2, "Tab 2")
        self.tab_widget.addTab(self.tab3, "Tab 3")

        # Add the tab widget to the central layout
        self.central_layout.addWidget(self.tab_widget)

        # Create grid layout for 3 viewing and 3d plot
        self.plot_grid = QGridLayout()

        # Create 3 viewings canvas widget
        self.plot_widget_0 = PlotWidget()
        self.plot_widget_1 = PlotWidget()
        self.plot_widget_2 = PlotWidget()

        # Create and add the vispy plot widget
        self.vispy_plot_widget = VispyPlotWidget()
        

        # Add 3 viewings plot and 3d plot to the grid layout
        self.plot_grid.addWidget(self.plot_widget_0,0,0)
        self.plot_grid.addWidget(self.plot_widget_1,1,0)
        self.plot_grid.addWidget(self.plot_widget_2,1,1)
        self.plot_grid.addWidget(self.vispy_plot_widget,0,1)

        # Set grid resizing behaviour
        self.plot_grid.setColumnStretch(0, 1)
        self.plot_grid.setColumnStretch(1, 1)
        self.plot_grid.setRowStretch(0, 1)
        self.plot_grid.setRowStretch(1, 1)

        # Minimize the spacing between widgets
        self.plot_grid.setSpacing(0)
        #self.plot_grid.setHorizontalSpacing(0)
        #self.plot_grid.setVerticalSpacing(0)
        
        # Minimize the margins around the layout
        self.plot_grid.setContentsMargins(0, 0, 0, 0)

        # Add grid layout to central layout
        self.central_layout.addLayout(self.plot_grid)

        # Create and add the slider widget
        self.slider_widget = SliderWidget(self.plot_widget_0)
        self.central_layout.addWidget(self.slider_widget)



        # Create and add widgets
        self.create_label()
        self.button_widget = CustomButton()  # Uses default label "Add"
        self.central_layout.addWidget(self.button_widget)

    def create_label(self):
        # Create a label and set its text
        label = QLabel("This is a GUI for meep")
        self.central_layout.addWidget(label)  # Add the label to the central layout



"""def main():
    # Create the application object
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Run the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
"""