from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QVBoxLayout

from prj.worker.Worker import Worker


class AsyncWidget(QWidget):

    work_trigger = pyqtSignal(int)
    trigger_button_style = "margin-left:180px;margin-right:180px;height:26px;border-radius:13px;background-color:rgb(0,180,144);font-weight:bold"
    trigger_button_style_1 = "margin-left:180px;margin-right:180px;height:26px;border-radius:13px;background-color:grey;font-weight:bold"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Async")
        self.init_ui()


    def init_ui(self):
        self.setMinimumWidth(600)
        self.trigger_btn = QPushButton("Trigger")
        self.trigger_btn.setStyleSheet(self.trigger_button_style)
        self.trigger_btn.clicked.connect(self.on_trigger_btn_clicked)
        self.progress_bar = QProgressBar()
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.trigger_btn)
        self.setLayout(layout)

        # self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.do_background()

    def on_trigger_btn_clicked(self):
        n = 100
        self.trigger_btn.setDisabled(True)
        self.trigger_btn.setStyleSheet(self.trigger_button_style_1)
        self.progress_bar.setMaximum(n)
        self.work_trigger.emit(n)

    def do_background(self):
        self.m_worker = Worker()
        self.m_worker_thread = QThread()
        self.m_worker.progress.connect(self.update_progress)
        self.work_trigger.connect(self.m_worker.do_work)
        self.m_worker.moveToThread(self.m_worker_thread)
        self.m_worker_thread.start()

    def update_progress(self, v):
        self.progress_bar.setValue(v)