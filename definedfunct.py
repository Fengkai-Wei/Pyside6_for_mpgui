import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QDialog, 
    QVBoxLayout, QTextEdit, QDialogButtonBox, QLabel, 
    QLineEdit
)
from PySide6.QtCore import Qt

import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        
        # 创建按钮
        self.button = QPushButton("Define Function", self)
        self.button.clicked.connect(self.open_function_dialog)
        self.setCentralWidget(self.button)

        # 存储用户定义的函数
        self.user_function = None

    def open_function_dialog(self):
        # 打开对话框
        dialog = FunctionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            # 获取用户定义的表达式和输入变量
            expression, param_names = dialog.get_function_code(), dialog.get_param_names()
            self.user_function = self.compile_function(expression, param_names)

            # 测试调用用户定义的函数
            if self.user_function:
                try:
                    # 创建测试参数
                    test_params = {name: float(input(f"Enter value for {name}: ")) for name in param_names}
                    result = self.user_function(**test_params)  # 使用关键字参数调用函数
                    print("Function result:", result)
                except Exception as e:
                    print(f"Error while executing the function: {e}")

    def compile_function(self, expression, param_names):
        """ 编译用户提供的表达式为函数 """
        local_vars = {}
        function_code = f"def user_function({', '.join(param_names)}):\n    return {expression}"
        try:
            exec(function_code, globals(), local_vars)
            return local_vars.get('user_function')
        except Exception as e:
            print(f"Error in user function code: {e}")
            return None

class FunctionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Define Function")

        # 创建文本编辑器
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Enter your expression here...\n\nExample:\n    x * y")

        # 创建输入框用于输入参数名
        self.param_names_edit = QLineEdit(self)
        self.param_names_edit.setPlaceholderText("Enter parameter names separated by commas\nExample: x, y")

        # 创建对话框按钮
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # 布局
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Define your expression below:"))
        layout.addWidget(self.text_edit)
        layout.addWidget(QLabel("Enter parameter names separated by commas:"))
        layout.addWidget(self.param_names_edit)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def get_function_code(self):
        """ 获取用户输入的表达式 """
        return self.text_edit.toPlainText().strip()

    def get_param_names(self):
        """ 获取用户输入的参数名 """
        return [name.strip() for name in self.param_names_edit.text().split(',')]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
