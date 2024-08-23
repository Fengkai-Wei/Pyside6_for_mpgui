from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from vispy import scene
import sys
import numpy as np

class VisPyPlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.canvas = None
        self.plot()

    def create_new_scene_canvas(self):
        # 创建新的 SceneCanvas
        canvas = scene.SceneCanvas(keys='interactive', bgcolor='white')
        view = canvas.central_widget.add_view()
        view.camera = 'turntable'

        # 添加图形示例：3D 散点图
        scatter = scene.visuals.Markers()
        data = np.random.normal(size=(100, 3))
        scatter.set_data(data, edge_color='blue', face_color='red', size=5)
        view.add(scatter)

        return canvas

    def remove_old_canvas(self):
        if self.canvas:
            self.layout().removeWidget(self.canvas.native)
            self.canvas.native.deleteLater()
            self.canvas = None

    def add_new_canvas(self, new_canvas):
        self.canvas = new_canvas
        self.layout().addWidget(self.canvas.native)

    def plot(self):
        # 移除旧的 SceneCanvas
        self.remove_old_canvas()

        # 创建新的 SceneCanvas
        new_canvas = self.create_new_scene_canvas()

        # 添加新的 SceneCanvas
        self.add_new_canvas(new_canvas)

        # 更新画布
        self.canvas.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建中心窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建 VisPyPlotWidget
        self.plot_widget = VisPyPlotWidget()
        layout.addWidget(self.plot_widget)

        # 创建按钮触发绘制新图形
        plot_button = QPushButton("Plot New Graph")
        plot_button.clicked.connect(self.plot_widget.plot)
        layout.addWidget(plot_button)

        self.setWindowTitle("VisPy Plot Example")
        self.resize(800, 600)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
