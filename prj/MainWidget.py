from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout

from prj.AsyncWidget import AsyncWidget


class MainWidget(QWidget):

    btn_style = "height:26px;border-radius:13px;background-color:rgb(0,180,144);font-weight:bold"

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.async_btn = QPushButton("Async Btn")
        layout = QHBoxLayout()
        layout.addWidget(self.async_btn)
        self.async_btn.setStyleSheet(self.btn_style)
        self.setLayout(layout)
        layout.setContentsMargins(220,0,220,100)
        self.async_window = None
        self.async_btn.clicked.connect(self.open_async_window)
    def open_async_window(self):
        if self.async_window is None:
            self.async_window = AsyncWidget()
            self.async_window.show()

