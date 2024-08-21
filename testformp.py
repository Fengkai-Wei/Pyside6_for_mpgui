import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QPoint, QRect

class DrawingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Draw Rectangle from Top-Left to Bottom-Right")
        self.setGeometry(0, 0, QApplication.primaryScreen().size().width(), QApplication.primaryScreen().size().height())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor("blue"))  # 设置矩形边框颜色为蓝色

        # 使用 QPoint 定位
        top_left = QPoint(0, 0)  # 左上角坐标
        bottom_right = QPoint(self.width(), self.height())  # 右下角坐标

        # 绘制矩形
        painter.drawRect(QRect(top_left, bottom_right))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个绘图小部件
        self.drawing_widget = DrawingWidget(self)
        self.setCentralWidget(self.drawing_widget)
        self.setWindowTitle("PySide6 Rectangle Drawing Example")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()  # 窗口全屏显示
    sys.exit(app.exec())
