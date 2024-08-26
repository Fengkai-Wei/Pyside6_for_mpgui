from PySide6.QtWidgets import QApplication, QLabel

app = QApplication([])

label = QLabel()

label.setText("E = mc<sup>2</sup> &alpha; + &beta; = &gamma; &times")  # 上标
label.show()

app.exec()
