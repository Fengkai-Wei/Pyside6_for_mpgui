from PySide6.QtWidgets import QApplication,QHeaderView, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QMenu, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
import meep as mp
mp.PML
class ButtonComboBox(QPushButton):
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.setText('Select an option')
        self.options = options
        
        # 创建一个菜单，并将按钮作为选项添加到菜单中
        self.menu = QMenu(self)
        self.setMenu(self.menu)
        self.setStyleSheet("QMenu { width: 100px; }")
        
        for option in options:
            action = QAction(option, self)
            action.triggered.connect(lambda checked, opt=option: self.on_option_selected(opt))
            self.menu.addAction(action)
    
    def on_option_selected(self, option):
        self.setText(option)
        print(f'i am {option}')

class TableWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建 QWidget 和布局
        layout = QVBoxLayout()

        # 创建 QTableWidget
        self.table_widget = QTableWidget()
        
        # 设置行数和列数
        self.table_widget.setRowCount(3)
        self.table_widget.setColumnCount(2)
        
        # 设置列标题
        self.table_widget.setHorizontalHeaderLabels(['Min', 'Max'])
        
        # 设置行标题
        self.table_widget.setVerticalHeaderLabels(['X', 'Y', 'Z'])
        
        # 创建按钮选项
        options = ['Option 1', 'Option 2', 'Option 3']
        
        # 将自定义 ButtonComboBox 添加到每个单元格中
        for row in range(3):
            for col in range(2):
                button_combo = ButtonComboBox(options=options)
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
        self.setLayout(layout)
        # 设置主窗口的中央部件


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建自定义的 TableWidget
        self.table_widget = TableWindow()

        # 将 TableWidget 添加到主窗口的中央部件中
        self.setCentralWidget(self.table_widget)

# 创建应用程序和主窗口
app = QApplication([])
window = MainWindow()
window.resize(400, 200)  # 设置窗口的初始尺寸
window.show()
app.exec()