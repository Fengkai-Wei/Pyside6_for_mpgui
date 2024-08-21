import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSlider, QWidget
from PySide6.QtCore import Qt
from vispy import scene
from vispy.color import Color
from vispy.app import use_app


class VisPyCanvas(scene.SceneCanvas):
    def __init__(self):
        super().__init__(keys=None, show=True, bgcolor='white')  # 设置背景透明
        self.unfreeze()

        # 添加ViewBox到canvas
        self.view = self.central_widget.add_view()
        self.view.camera = 'turntable'  # 设置相机类型

        # 生成随机数据
        self.data = np.random.rand(100, 3)
        self.scatter = scene.visuals.Markers()
        self.scatter.set_data(self.data, face_color='red', size=5)
        self.view.add(self.scatter)
        self.axis = scene.visuals.XYZAxis(parent=self.view.scene)
        self.freeze()

    def update_canvas(self, value):
        """Update the canvas when the slider value changes."""
        # 更新随机数据的大小或位置
        self.data = np.random.rand(100, 3) * (value / 10)
        self.scatter.set_data(self.data,face_color = 'red',size =5)
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisPy and PySide6 Example")

        # 创建主widget
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        # 创建VisPy画布
        self.canvas = VisPyCanvas()
        layout.addWidget(self.canvas.native)  # 使用canvas的原生widget

        # 创建滑块
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 100)  # 设置滑块范围
        self.slider.setValue(10)  # 设置滑块初始值
        layout.addWidget(self.slider)

        # 连接滑块的值变化信号到canvas更新函数
        self.slider.valueChanged.connect(self.canvas.update_canvas)


if __name__ == "__main__":
    # 必须明确使用PyQt/PySide后端
    use_app('pyside6')  # 或 'pyside6'
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
