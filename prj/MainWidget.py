from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):

        self.btn = QPushButton("Async Btn")
        layout = QHBoxLayout()
        layout.addWidget(self.btn)
        self.setLayout(layout)
