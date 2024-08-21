import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QPoint, QEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建 Matplotlib 图形和画布
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setFixedHeight(30)  # 设置工具栏的高度

        # 布局管理
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        # 启用鼠标事件处理
        self.canvas.setFocusPolicy(Qt.ClickFocus)
        self.canvas.installEventFilter(self)

        # 示例绘图
        self.ax.plot([0, 1, 2, 3], [10, 1, 20, 3])
        self.canvas.draw()  # 确保画布初始化时绘图

        # 其他初始化代码
        self.panning = False
        self.zooming = False
        self.last_pos = None

    def eventFilter(self, obj, event):
        if obj is self.canvas:
            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.panning = True
                    self.last_pos = event.pos()
                    self.toolbar.pan()  # 启动平移模式
            elif event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    self.panning = False
                    self.last_pos = None
                    self.toolbar.home()  # 退出平移模式
            elif event.type() == QEvent.MouseMove:
                if self.panning and self.last_pos:
                    current_pos = event.pos()
                    delta = current_pos - self.last_pos
                    # 更新画布（可能需要将 `self.on_motion_notify` 处理逻辑放在这里）
                    self.last_pos = current_pos
                    self.canvas.draw()  # 确保画布在拖拽过程中更新
            elif event.type() == QEvent.Wheel:
                delta = event.angleDelta().y()
                if delta > 0:
                    self.toolbar.zoom('in')  # 向上滚动，放大
                else:
                    self.toolbar.zoom('out')  # 向下滚动，缩小
                self.canvas.draw()  # 确保画布在缩放后更新
            return True
        return super().eventFilter(obj, event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建 MatplotlibWidget 实例并设置为中心窗口部件
        self.mpl_widget = MatplotlibWidget(self)
        self.setCentralWidget(self.mpl_widget)

        self.setWindowTitle("PySide6 Matplotlib Example")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
