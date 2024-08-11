import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFormLayout, 
    QDoubleSpinBox, QLabel, QLineEdit
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FormLayout with Signal Example")

        # 示例 dict
        sample_dict = {
            "coordinate": [1.0, 2.0, 3.0],  # 三维坐标
            "text": "Example text",  # 文本
            "value": 42.0,  # 单个数值
        }

        # 创建主窗口小部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 创建 FormLayout
        layout = QFormLayout(main_widget)

        # 根据字典中的值类型动态创建 QWidget 并添加到布局中
        for key, value in sample_dict.items():
            widget = self.create_widget_for_value(value)
            layout.addRow(QLabel(f"{key}:"), widget)

    def create_widget_for_value(self, value):
        """根据值的类型返回相应的 QWidget"""
        if isinstance(value, (list, tuple, np.ndarray)) and len(value) == 3:
            return self.create_coordinate_widget(value)
        elif isinstance(value, str):
            return self.create_text_widget(value)
        elif isinstance(value, (int, float)):
            return self.create_number_widget(value)
        else:
            return QLabel("Unsupported type")

    def create_coordinate_widget(self, value):
        """为三维坐标生成一个 QWidget"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        for i in range(3):
            spin_box = QDoubleSpinBox()
            spin_box.setValue(value[i])
            # 连接信号到槽函数
            spin_box.valueChanged.connect(self.on_value_changed)
            layout.addRow(QLabel(f"Coordinate {i+1}:"), spin_box)
        
        return widget

    def create_text_widget(self, value):
        """为字符串生成一个 QWidget"""
        line_edit = QLineEdit()
        line_edit.setText(value)
        # 连接信号到槽函数
        line_edit.textChanged.connect(self.on_text_changed)
        return line_edit

    def create_number_widget(self, value):
        """为单个数值生成一个 QWidget"""
        spin_box = QDoubleSpinBox()
        spin_box.setValue(value)
        # 连接信号到槽函数
        spin_box.valueChanged.connect(self.on_value_changed)
        return spin_box

    def on_value_changed(self, value):
        """处理 QDoubleSpinBox 的值改变信号"""
        print(f"Value changed: {value}")

    def on_text_changed(self, text):
        """处理 QLineEdit 的文本改变信号"""
        print(f"Text changed: {text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
