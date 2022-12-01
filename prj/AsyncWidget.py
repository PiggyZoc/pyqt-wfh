import os.path
import time

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
        self.filename = "large.log"
        self.progress_num = 0
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
        # self.do_background()

    def on_trigger_btn_clicked(self):
        s = time.time()
        self.trigger_btn.setDisabled(True)

        self.trigger_btn.setStyleSheet(self.trigger_button_style_1)

        self.progress_bar.setMaximum(self.get_line_num())
        big_file = open(self.filename, "r")
        # # 950
        file_size = os.path.getsize("large.log")

        BUF_SIZE = file_size // 8
        tem_lines = big_file.readlines(BUF_SIZE)
        self.workers = []
        self.worker_threads = []
        while tem_lines:
            worker = Worker(buf=tem_lines)
            worker.progress.connect(self.update_progress)
            worker_thread = QThread()
            worker.moveToThread(worker_thread)
            worker_thread.started.connect(worker.do_work)
            worker_thread.start()
            self.workers.append(worker)
            self.worker_threads.append(worker_thread)
            # print(tem_lines[-1].replace("\n",""))
            # for line in tem_lines:
            #     pool.submit(_process, line.replace("\n", ""))
            tem_lines = big_file.readlines(BUF_SIZE)
        print(f"Elapsed: {time.time() - s}")
        # self.progress_bar.setMaximum(n)
        # self.work_trigger.emit(n)

    def get_line_num(self):
        big_file = open(self.filename, "r")
        # # 950
        file_size = os.path.getsize("large.log")

        BUF_SIZE = file_size // 18

        tem_lines = big_file.readlines(BUF_SIZE)
        num = 0
        while tem_lines:
            num += len(tem_lines)
            # for line in tem_lines:
            #     pool.submit(_process, line.replace("\n", ""))
            tem_lines = big_file.readlines(BUF_SIZE)
        return num
    # def do_background(self):
    #     self.m_worker = Worker()
    #     self.m_worker_thread = QThread()
    #     self.m_worker.progress.connect(self.update_progress)
    #     self.work_trigger.connect(self.m_worker.do_work)
    #     self.m_worker.moveToThread(self.m_worker_thread)
    #     self.m_worker_thread.start()

    def update_progress(self, v):
        self.progress_num += 1
        self.progress_bar.setValue(self.progress_num)