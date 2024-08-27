import sys
import numpy as np
import meep as mp

from PySide6.QtWidgets import (QSizePolicy,QTableWidget,QCheckBox, QMainWindow,QHeaderView, QLabel,QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,QToolTip, QListWidget, QListWidgetItem, QMenu, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QSlider, QDoubleSpinBox, QTabWidget, QGridLayout)
from PySide6.QtGui import QAction, QFontMetrics, QCursor
from PySide6.QtCore import QTimer, QPoint,Qt
import copy
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backend_bases import MouseEvent

mpl.rcParams['savefig.pad_inches'] = 0

from vispy import scene
from vispy.scene import visuals

import global_vars
from var_manage import add_var, rm_var
global_vars.init()
from  global_vars import var_dict,reverse_dict,reload_BC

mp.verbosity(0)


from PySide6.QtWidgets import QWidget, QHBoxLayout, QDoubleSpinBox, QLabel
from PySide6.QtCore import Signal, Qt

class BoundaryDialog(QDialog):
    def __init__(self,side,dir,pml_type,parent=None):
        super().__init__(parent)
        self.parent = parent
        self.side = side
        self.dir = dir
        self.type = pml_type
        self.mp_dir = var_dict['direction'][self.dir]
        self.mp_side = var_dict['side'][self.side]

        self.same_dir = self.parent.parent.same_dir
        self.all_dir = self.parent.parent.all_dir

        self.setWindowTitle(f'{type(self.type).__name__} Layer{self.dir, self.side}')

        # Create layout
        layout = QFormLayout(self)
        self.current_bc = None
        for item in var_dict['Boundary']:
            if item.direction == self.mp_dir and item.side == self.mp_side:
                self.current_bc = item


        for key,val in self.type.__dict__.items():
            show_attr = key

            if key[0] == '_':
                show_attr = key[1:]
            
            if show_attr == 'thickness':
                self.thickness = QDoubleSpinBox()
                self.thickness.setValue(self.current_bc.thickness if self.current_bc else 0.1)
                layout.addRow(f'{show_attr.capitalize()}:',self.thickness)
            elif show_attr == 'direction':
                self.dircombo = QLabel(self.dir)
                layout.addRow(f'{show_attr.capitalize()}:',self.dircombo)
            elif show_attr == 'side':
                self.sidecombo = QLabel(self.side)
                layout.addRow(f'{show_attr.capitalize()}:',self.sidecombo)
            elif show_attr == 'R_asymptotic':
                self.r = QLineEdit()
                r_asymp = self.current_bc._R_asymptotic if self.current_bc else 1e-15
                self.r.setText(str(r_asymp))

                layout.addRow(f'R Asymptotic:',self.r)
            elif show_attr == 'pml_profile':
                self.pml_btn = QPushButton('View && Edit')
                self.pml = self.current_bc.pml_profile if self.current_bc else None

                self.pml_btn.setStyleSheet("color: blue; font-weight: bold;")
                layout.addRow(f'PML Profile:',self.pml_btn)
            else:
                continue
        
        self.same_dir_check = QCheckBox()
        self.same_dir_check.setChecked(self.same_dir)
        self.same_dir_check.setEnabled(not self.all_dir)
        

        self.all_dir_check = QCheckBox()
        self.all_dir_check.setChecked(self.all_dir)

        layout.addRow(f'BOTH side of {self.dir}:',self.same_dir_check)
        layout.addRow('ALL XYZ directions:',self.all_dir_check)

        self.all_dir_check.stateChanged.connect(self.same_all_switch)

        self.button_clear = QPushButton('Clear')
        self.button_clear.setStyleSheet("color: red; font-weight: bold;")
        self.button_clear.clicked.connect(self.clear)

        self.button_submit = QPushButton('Submit')
        self.button_submit.clicked.connect(self.submit)


        layout.addRow(self.button_submit)
        layout.addRow(self.button_clear)

    def same_all_switch(self):
        if self.all_dir_check.isChecked():
            self.same_dir_check.setEnabled(False)

        else:
            self.same_dir_check.setEnabled(True)

    def submit(self):
        if self.all_dir_check.isChecked():
            self.parent.parent.all_dir = True
            var_dict['Boundary'] = []
            var_dict['Boundary'].append(self.type.__class__(thickness = self.thickness.value(),
                                                            R_asymptotic = eval(self.r.text()) if eval(self.r.text()) <= 1e-15 else 1e-15,
                                                            direction = mp.ALL,
                                                            side = mp.ALL))
            
        elif self.same_dir_check.isChecked():
            self.parent.parent.same_dir = True
            self.parent.parent.all_dir = False
            for item in var_dict['Boundary']:
                if item.direction == self.mp_dir or item.direction == mp.ALL:
                    var_dict['Boundary'].remove(item)
            var_dict['Boundary'].append(self.type.__class__(thickness = self.thickness.value(),
                                                            R_asymptotic = eval(self.r.text()) if eval(self.r.text()) <= 1e-15 else 1e-15,
                                                            direction = self.mp_dir,
                                                            side = mp.ALL))
        
        else:
            self.parent.parent.same_dir = False
            self.parent.parent.all_dir = False

            for item in var_dict['Boundary']:
                if (item.direction == mp.ALL) or (item.direction == self.mp_dir and item.side == mp.ALL):
                    var_dict['Boundary'].remove(item)
                elif item.direction == self.mp_dir and item.side == self.mp_side:
                    item.thickness = self.thickness.value()
                    item._R_asymptotic = eval(self.r.text()) if eval(self.r.text()) <= 1e-15 else 1e-15
                    item.pml_profile = self.pml if self.pml else None

                    super().accept()
                    return
            
            var_dict['Boundary'].append(self.type.__class__(thickness = self.thickness.value(),
                                                            direction = self.mp_dir,
                                                            R_asymptotic = eval(self.r.text()) if eval(self.r.text()) <= 1e-15 else 1e-15,
                                                            side = self.mp_side))
            self.parent.setText(f'{type(self.type).__name__}, Thickness = {self.thickness.value()}')
            super().accept()
        


    
    def clear(self):
        for item in var_dict['Boundary']:
            if item.direction == self.mp_dir and item.side == self.mp_side:
                var_dict['Boundary'].remove(item)
                break
        self.parent.setText('No PML')
        super().accept()

class ButtonComboBox(QPushButton):
    def __init__(self, options, direction, side, parent=None):
        super().__init__(parent)
        self.setText('No PML')
        self.options = options
        self.parent = parent
        self.same_dir = self.parent.same_dir
        self.all_dir = self.parent.all_dir
        # 创建一个菜单，并将按钮作为选项添加到菜单中
        self.menu = QMenu(self)
        self.setMenu(self.menu)


        
        for option in options:
            action = QAction(option, self)
            action.triggered.connect(lambda checked, opt=option: self.on_option_selected(opt,direction,side))
            self.menu.addAction(action)
    
    def on_option_selected(self, option,dir,side):
        #self.setText(option)
        print(f'I am {option} at {dir}.{side}')

        

        if option == 'Metallic' or option == 'Magnetic':
            
            var_dict['CurrentSim'].set_boundary(side = var_dict['side'][side],
                                                direction = var_dict['direction'][dir],
                                                condition = var_dict['boundary_condition'][option])
 

            
        elif option == 'PML' or option == 'Absorber':
            dialog = BoundaryDialog(dir = dir,
                                    side = side, 
                                    pml_type = mp.PML(thickness = 0.1) if option == 'PML' else mp.Absorber(thickness = 0.1),
                                    parent = self)
            if dialog.exec():

                pass
        elif option == 'Periodic':
            pass

class BoundaryTable(QWidget):
    def __init__(self):
        super().__init__() 

        self.same_dir = False
        self.all_dir = False

        # 创建 QWidget 和布局
        layout = QVBoxLayout()

        # 创建 QTableWidget
        self.table_widget = QTableWidget()
        
        # 设置行数和列数
        self.table_widget.setRowCount(3)
        self.table_widget.setColumnCount(2)
        
        # 设置列标题
        col_list = ['Low', 'High']
        self.table_widget.setHorizontalHeaderLabels(col_list)
        
        # 设置行标题
        row_list = ['X', 'Y', 'Z']
        self.table_widget.setVerticalHeaderLabels(row_list)
        
        # 创建按钮选项
        options = ['PML', 'Absorber(PML)', 'Periodic', 'Metallic', 'Magnetic']
        
        # 将自定义 ButtonComboBox 添加到每个单元格中
        for row in range(3):
            for col in range(2):
                button_combo = ButtonComboBox(side=col_list[col],
                                              direction = row_list[row],
                                              options=options,
                                              parent=self)
                self.table_widget.setCellWidget(row, col, button_combo)

        # 设置表头字体为粗体
        self.table_widget.horizontalHeader().setStyleSheet("font-weight: bold;")
        self.table_widget.verticalHeader().setStyleSheet("font-weight: bold;")

        # 设置行高和列宽
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 设置表格的列宽和行高可以自动调整
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 将表格添加到布局中
        layout.addWidget(self.table_widget)
        
        # 设置主窗口的中央部件

        self.setLayout(layout)
    def update_BC_table(self):
        for item in var_dict['Boundary']:
            if item.direction  == mp.ALL:
                for row in range(self.table_widget.rowCount()):
                    for column in range(self.table_widget.columnCount()):
                        cell = self.table_widget.item(row=row,column=column)
                        cell.setText(f'{type(cell.type).__name__}, ')

                break

            else:
                pass




class PositionWidget(QWidget):
    # Signal emitted when any of the spinboxes change value
    position_changed = Signal(float, float, float)

    def __init__(self, position=None, parent=None):
        super().__init__(parent)
        self.setLayout(QHBoxLayout())

        # Initialize position
        position = position or [0.0, 0.0, 0.0]

        # Create spinboxes
        self.x_spinbox = QDoubleSpinBox()
        self.y_spinbox = QDoubleSpinBox()
        self.z_spinbox = QDoubleSpinBox()

        # Set initial values
        self.x_spinbox.setValue(position[0])
        self.y_spinbox.setValue(position[1])
        self.z_spinbox.setValue(position[2])

        # Connect valueChanged signals to a common handler
        self.x_spinbox.valueChanged.connect(self.on_value_changed)
        self.y_spinbox.valueChanged.connect(self.on_value_changed)
        self.z_spinbox.valueChanged.connect(self.on_value_changed)

        # Add labels and spinboxes to the layout
        self.layout().addWidget(QLabel("X:"))
        self.layout().addWidget(self.x_spinbox)
        self.layout().addWidget(QLabel("Y:"))
        self.layout().addWidget(self.y_spinbox)
        self.layout().addWidget(QLabel("Z:"))
        self.layout().addWidget(self.z_spinbox)

    def on_value_changed(self):
        # Emit the position_changed signal with the new position
        x = self.x_spinbox.value()
        y = self.y_spinbox.value()
        z = self.z_spinbox.value()
        self.position_changed.emit(x, y, z)

    def get_position(self):
        """Return the current position as a list of [x, y, z]."""
        return [self.x_spinbox.value(), self.y_spinbox.value(), self.z_spinbox.value()]

    def set_position(self, position):
        """Set the position to the specified [x, y, z] values."""
        self.x_spinbox.setValue(position[0])
        self.y_spinbox.setValue(position[1])
        self.z_spinbox.setValue(position[2])





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
        #self.setGeometry(100, 100, 300, 100)
        self.combo_list = combo_list
        self.type = type
        self.setWindowTitle(f'Add {self.type}')

        # Create layout
        layout = QFormLayout(self)

        # Create input for name of new item
        self.name_input = QLineEdit()
        self.name_input.setText(f'New_{self.type}')
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
        print(f"Combo input changed: {new_text}")
    def get_values(self):
        return {'name':self.name_input.text(),
                'type':self.type_combo.currentText()}





class CustomEditDialog(QDialog):
    def __init__(self, item_text,plot_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Item")
        #self.setGeometry(100, 100, 300, 200)
        self.parent = parent
        self.plot_list = plot_list

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
        
        # Create a name input
        self.text_input = QLineEdit()
        self.text_input.setText(self.item_text)
        layout.addRow("Text:", self.text_input)
        self.text_input.textChanged.connect(self.on_text_changed)


        

        # Get all attr of object
        parent.print_list_items()
        print(self.target_dict[self.item_text].__dict__)
        attr_list = self.target_dict[self.item_text].__dict__
        for (key,value) in attr_list.items():
            # print(key,value)

            if key == 'label':
                continue

            widget = QWidget()
            
            if isinstance(value, str):
                widget = QLineEdit(value)
                widget.textChanged.connect(self.on_val_changed)
            elif isinstance(value, int):
                widget = QSpinBox()
                widget.setValue(value)
                widget.valueChanged.connect(self.on_val_changed)
            elif isinstance(value, float):
                widget = QDoubleSpinBox()
                widget.setValue(value)
                widget.valueChanged.connect(self.on_val_changed)
            elif isinstance(value, mp.Vector3):
                widget = PositionWidget(value)
                widget.position_changed.connect(self.on_position_changed)
                pass

            elif isinstance(value, mp.Medium):
                widget = QComboBox()
                current_mat = reverse_dict(from_dict=var_dict['Material'],
                                           find_val=value)
                
                
                widget.addItems(list(var_dict['Material'].keys()))
                widget.setMaxVisibleItems(15)
                widget.setStyleSheet("QComboBox { combobox-popup: 0; }")
                widget.setCurrentText(current_mat)
                widget.currentTextChanged.connect(self.on_val_changed)
            else:
                widget = QLabel(type(value).__name__)
                

            widget.label = key
            temp_key = key[1:] if key[0] == '_' else key
            layout.addRow(f'{temp_key.capitalize()}:',widget)
            


       
        




        # Create buttons
        self.button_box = QPushButton("OK")
        self.button_box.clicked.connect(self.check_name)
        layout.addRow(self.button_box)

        self.setLayout(layout)

    def get_name(self):
        return self.text_input.text()

    def on_text_changed(self, new_text):

        #self.target_dict.clear()



        print(self.target_dict == var_dict['geo'])


        

        self.target_dict[new_text] = self.target_dict.pop(self.item_text)


        print(self.target_dict == var_dict['geo'])

        self.item_text = new_text
        print(self.item_text)
        self.parent.print_list_items(if_print= True)
        print(f"Text input changed: {new_text}")

    
    def on_val_changed(self,new_val):
        sender = self.sender()
        
        if sender.label == 'material': 
            self.target_dict[self.item_text].__dict__[sender.label] = var_dict['Material'][new_val]
        else:
            self.target_dict[self.item_text].__dict__[sender.label] = new_val

        for sub_plot in self.plot_list:
            sub_plot.plot()
        
        print(f'new value: {new_val}')


    def on_position_changed(self, x, y, z):
        sender = self.sender()
        self.target_dict[self.item_text].__dict__[sender.label]=mp.Vector3(x,y,z)

        for sub_plot in self.plot_list:
            sub_plot.plot()
        print('plot')
        print(f'current pos is: {x, y, z}')

    def check_name(self):
        if self.text_input.text() == self.item_text:
            super().accept()

        elif self.text_input.text() in self.parent.print_list_items():
            self.msg =  CustomMsgBox(self)
            self.msg.show_msg(
                title = 'Invalid Name',
                message = f"{self.text_input.text()} is already named",
                icon = QMessageBox.Warning,
                buttons = QMessageBox.Ok
            )
        else:
            super().accept()

class CustomListWidget(QWidget):
    def __init__(self, add_type = 'Structure', add_combo=var_dict['Structure'] ,items=None, parent=None):
        super().__init__(parent)
        if items is None:
            items = []
        self.list_items = items
        self.add_combo = add_combo
        self.add_type = add_type
        self.plot_list = [self.parent().plot_widget_0, self.parent().plot_widget_1, self.parent().plot_widget_2, self.parent().vispy_plot_widget]
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
        self.list_widget.model().rowsMoved.connect(lambda: self.print_list_items(if_reorder = True))
        self.list_widget.model().rowsRemoved.connect(lambda: self.print_list_items(if_reorder = True))
        self.list_widget.model().rowsInserted.connect(lambda: self.print_list_items())

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

                # always force the material is defined from var_dict['Material']
                temp_obj.material = var_dict['Material']['Vaccum']
                temp_obj.label = values['name']
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
            dialog = CustomEditDialog(item_text=self.current_item.text(), plot_list=self.plot_list,parent=self)
            if dialog.exec():
                name = dialog.get_name()

                if self.current_item.text() == name:
                    pass
                else:
                    # Get current list of item
                    current_list = self.print_list_items()

                    # Check if duplicate
                    if name in current_list:

                        self.msg =  CustomMsgBox(self)
                        self.msg.show_msg(
                            title = 'Invalid Name',
                            message = f"{name} is already named",
                            icon = QMessageBox.Warning,
                            buttons = QMessageBox.Ok
                        )
                        
                    else:
                        self.current_item.setText(name)

    def delete_item(self):
        # Permanently delete the item
        if hasattr(self, 'current_item'):
            row = self.list_widget.row(self.current_item)
            item = self.list_widget.item(row).text()
            self.list_widget.takeItem(row)
            
            if self.add_type == 'Structure':

                var_dict['geo'].pop(item)
                print(f'Geometry: {var_dict["geo"].keys()}')

            elif self.add_type == 'Sources':

                var_dict['src'].pop(item)
                print(f'Sources: {var_dict["src"].key()}')
            
            elif self.add_type == 'Monitors':
                pass

            self.print_list_items()

    def copy_item(self):
        # Copy the item text to the end of the list
        if hasattr(self, 'current_item'):
            new_item_text = f"{self.current_item.text()}_0"
            counter = 0
            list = self.print_list_items()
            while new_item_text in list:
                counter += 1
                new_item_text = f"{self.current_item.text()}_{counter}"


            
            if self.add_type == 'Structure':

                copy_obj = var_dict['geo'][self.current_item.text()]
                var_dict['geo'].update({new_item_text:copy_obj})
                print(f'Geometry: {var_dict["geo"].keys()}')

            elif self.add_type == 'Sources':

                copy_obj = var_dict['src'][self.current_item.text()]
                var_dict['src'].update({new_item_text:copy_obj})
                print(f'Sources: {var_dict["src"].keys()}')
            
            elif self.add_type == 'Monitors':
                pass
            
            print(new_item_text)
            self.list_widget.addItem(new_item_text)
            self.print_list_items()

    def print_list_items(self, if_print = False, if_reorder = False):
        # Print all items in the list
        list_items = []
        print("Current list items:")
        for index in range(self.list_widget.count()):
            list_items.append(self.list_widget.item(index).text())
        if if_print:
            print(list_items)
        if if_reorder:
            if self.add_type == 'Structure':

                var_dict['geo'] = {key: var_dict['geo'][key] for key in list_items}

            elif self.add_type == 'Sources':

                var_dict['src'] = {key: var_dict['src'][key] for key in list_items}

            elif self.add_type == 'Monitors':
                pass


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
    def __init__(self, output_plane: mp.simulation.Volume, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.output_plane = output_plane

        # Create a matplotlib figure and axis
        self.figure, self.ax = plt.subplots()

        # Ensure a tight layout
        #self.figure.tight_layout()
        
        # Create a FigureCanvas object
        self.canvas = FigureCanvas(self.figure)

        # Create a toolbar 
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.hide()
        # Real time position
        #self.toolbar.update()

        # Create a QVBoxLayout for this widget
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)  # Set the layout for this widget

        # Add the canvas to the layout
        self.layout.addWidget(self.canvas)

        # Plot some example data
        #self.plot()

        # Remove all paddings
        self.figure.subplots_adjust(top=0.99,
                            bottom=0.01,
                            left=0.01,
                            right=0.99)
        
        # Set xticks and ytick on other side of axis
        self.ax.tick_params(axis='both', which='both', direction='in', labelbottom=False, labeltop=False, labelleft=False, labelright=False)

        # Add right-click menu to canvas object
        self.canvas.setContextMenuPolicy(Qt.CustomContextMenu)  # Qt.CustomContextMenu
        self.canvas.customContextMenuRequested.connect(self.show_context_menu)

        # Create right-click menu
        self.context_menu = QMenu(self)
        
        # Add toolbar functionality to right-click menu
        self.add_toolbar_actions()
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)


        self.tooltip_text = ""

        self.show_tooltip = False


    def on_mouse_move(self, event: MouseEvent):
        if event.inaxes != self.ax:
            QToolTip.hideText()
            return

        # 获取鼠标数据坐标
        x, y = event.xdata, event.ydata
        self.tooltip_text = f"x: {x:.2f}, y: {y:.2f}"

        # 更新工具提示
        self.update_tooltip()

    def update_tooltip(self):
        """ Update the tooltip text based on the latest mouse position. """
        # 直接显示工具提示文本，而不更新位置
        QToolTip.showText(self.mapToGlobal(QPoint(0,0)), self.tooltip_text, self.canvas)


    def leaveEvent(self, event):
        super().leaveEvent(event)
        # 鼠标离开时取消工具提示
        QToolTip.hideText()

    def add_toolbar_actions(self):
        # Add toolbar functionalities to right-click menu 
        
        self.add_action("Save Figure", self.save_figure)
        self.add_action("Home", self.home)
        self.add_action("Back", self.back)
        self.add_action("Forward", self.forward)
        self.add_action("Print Figure", self.print_figure)

    def add_action(self, text, slot):
        action = QAction(text, self)
        action.triggered.connect(slot)
        self.context_menu.addAction(action)

    def show_context_menu(self, point):
        self.context_menu.exec(self.canvas.mapToGlobal(point))

    def save_figure(self):
        self.toolbar.save_figure()
        self.update()

    def home(self):
        self.toolbar.home()
        self.update()

    def back(self):
        self.toolbar.back()
        self.update()

    def forward(self):
        self.toolbar.forward()
        self.update()

    def print_figure(self):
        self.toolbar.print_figure()
        self.update()


    def plot(self, scale=1):
        # Clear previous plot

        if var_dict['geo'] or var_dict['src'] or var_dict['dft']:
            geometry = list(var_dict['geo'].values())
            print(var_dict['geo'].items())
            print(var_dict['geo'].values())
            sources = list(var_dict['src'].values())
            dft_objects = list(var_dict['dft'].values())
            sim = var_dict['CurrentSim']
            sim.geometry = geometry
            sim.sources = sources
            sim.dft_object = dft_objects
            sim.boundary_layers = var_dict['Boundary']

            self.ax.clear()
            sim.plot2D(ax = self.ax, output_plane = self.output_plane,labels =False,label_geometry = False)
        


            self.ax.grid(color=(0,0,0,0.1), linestyle='--')
            # Example plot with dynamic scaling
            #x = [1, 2, 3, 4]
            #y = [1, 4, 9, 16]
            #self.ax.plot(x, [i * scale for i in y], 'r-')
            self.ax.set_xlabel('')
            self.ax.set_ylabel('')
            #self.ax.set_xlim([-6, 6])
            #self.ax.set_xticks(np.arange(-6, 6, 1))
            #self.ax.set_ylim([-16*scale, 16*scale])
            #self.ax.set_yticks(np.arange(-16*scale, 16*scale, 16))

            """
            self.ax.spines['left'].set_position('center')
            self.ax.spines['bottom'].set_position('center')

            # Eliminate upper and right axes
            self.ax.spines['right'].set_color('none')
            self.ax.spines['top'].set_color('none')

            # Show ticks in the left and lower axes only
            self.ax.xaxis.set_ticks_position('bottom')
            self.ax.yaxis.set_ticks_position('left')
            """


                


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
        self.canvas = scene.SceneCanvas(keys='interactive',
                                        show=True,
                                        bgcolor='white')
        
        
        # Create a view
        self.view = self.canvas.central_widget.add_view()
        
        # Create 3D axis
        self.view.camera = 'turntable'
        xyz_axis = visuals.XYZAxis(parent=self.view.scene)
        xyz_axis._width = 3
        # Add data
        # self.plot()

        # Create a QVBoxLayout for this widget
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        
        # Add the canvas to the layout
        self.layout.addWidget(self.canvas.native)

        # Freeze when not calling for plot 
        self.canvas.update()
        self.canvas.freeze()

    def plot(self):

        if var_dict['CurrentSim']:

            self.canvas.unfreeze()
            
            # Get canvas and view from plot3D
            mp_view = var_dict['CurrentSim'].plot3D().central_widget.children[0]
            
            # Clear old view in canvas
            self.canvas.central_widget.remove_widget(self.view)

            # Redefine the view from visapy plot
            self.view = mp_view
            
            # Add axis
            xyz_axis = visuals.XYZAxis(parent=self.view.scene)
            xyz_axis._width = 3

            # Add new ViewBox to old canvax
            self.canvas.central_widget.add_widget(self.view)






            """
            for visuals in mp_view.children:
                if isinstance(visuals, scene.visuals.Visual):
                    new_visual  = visuals.__class__(**visuals._params)
                    self.view.add(new_visual)
            """
            
            # Update the canvas
            self.canvas.update()

            
            

        

            self.canvas.freeze()
    
    def mp_canvas(self):
        if var_dict['CurrentSim']:
            
            canvas = var_dict['CurrentSim'].plot3D()
            view = canvas.central_widget.add_view()
            view.camera = 'turntable'

            

        



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Application")
        #self.setGeometry(0, 0, 1000, 1000)  # Adjust window size for layout



        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create and configure layouts
        self.central_layout = QVBoxLayout(central_widget)


        # Create grid layout for 3 viewing and 3d plot
        self.plot_grid = QGridLayout()

        # Create 3 viewings canvas widget

        # Get cell_size and geometric_center of current simmulation object
        size, center = var_dict['CurrentSim'].cell_size, var_dict['CurrentSim'].geometry_center

        size_mat = np.array(size)*np.array([[1,1,0],
                                            [0,1,1],
                                            [1,0,1]])
        self.plot_widget_0 = PlotWidget(output_plane=mp.simulation.Volume(size = size_mat[0],center = center))
        self.plot_widget_1 = PlotWidget(output_plane=mp.simulation.Volume(size = size_mat[1],center = center))
        self.plot_widget_2 = PlotWidget(output_plane=mp.simulation.Volume(size = size_mat[2],center = center))

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

        self.tab_widget = QTabWidget()

        # Create and add tabs
        self.tab1 = CustomListWidget(parent=self)
        self.tab2 = CustomListWidget(add_type= 'Sources', add_combo= var_dict['Sources'],parent=self)
        self.tab3 = CustomListWidget(parent=self)
        self.tab4 = BoundaryTable()

        self.tab_widget.addTab(self.tab1, "Structures")
        self.tab_widget.addTab(self.tab2, "Sources")
        self.tab_widget.addTab(self.tab3, "Monitors")
        self.tab_widget.addTab(self.tab4, "Boundaries")

        # Add the tab widget to the central layout
        self.central_layout.addWidget(self.tab_widget)

        # Add grid layout to central layout
        self.central_layout.addLayout(self.plot_grid)

        # Create and add the slider widget
        self.slider_widget = SliderWidget(self.plot_widget_1)
        self.central_layout.addWidget(self.slider_widget)


        # Create and add widgets
        self.create_label()
        self.button_widget = CustomButton()  # Uses default label "Add"
        self.central_layout.addWidget(self.button_widget)

    def create_label(self):
        # Create a label and set its text
        label = QLabel("This is a GUI for meep")
        self.central_layout.addWidget(label)  # Add the label to the central layout