from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout

from prj.AsyncWidget import AsyncWidget
from prj.LintCheckWidget import LintCheckWin
from prj.SocAsyncListWidget import SocAsyncListWin


class MainWidget(QWidget):
    btn_style = "height:26px;border-radius:13px;background-color:rgb(255, 239, 0);font-weight:bold"

    def __init__(self):
        super().__init__()
        self.lint_check_btn = None
        self.soc_async_list_btn = None
        self.lint_check_win = None
        self.soc_async_list_win = None
        self.init_ui()

    def init_ui(self):
        self.lint_check_btn = QPushButton("Lint Check")
        self.soc_async_list_btn = QPushButton("Soc Async List")
        layout = QVBoxLayout()
        layout.addWidget(self.lint_check_btn)
        layout.addWidget(self.soc_async_list_btn)
        self.lint_check_btn.setStyleSheet(self.btn_style)
        self.soc_async_list_btn.setStyleSheet(self.btn_style)
        self.setLayout(layout)
        layout.setContentsMargins(220, 0, 220, 300)
        self.lint_check_btn.clicked.connect(self.open_lint_check_win)
        self.soc_async_list_btn.clicked.connect(self.open_async_window)
        # self.async_btn.clicked.connect(self.open_async_window)

    def open_lint_check_win(self):
        if self.lint_check_win is None:
            self.lint_check_win = LintCheckWin()
            self.lint_check_win.close_signal.connect(self.close_window)
            self.lint_check_win.show()

    def open_async_window(self):
        if self.soc_async_list_win is None:
            self.soc_async_list_win = SocAsyncListWin()
            self.soc_async_list_win.close_signal.connect(self.close_window)
            self.soc_async_list_win.show()


    @pyqtSlot(str)
    def close_window(self, name):
        if name == 'lint':
            self.lint_check_win = None
        elif name == 'soc':
            self.soc_async_list_win = None
