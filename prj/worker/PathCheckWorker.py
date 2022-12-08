import os

from PyQt5.QtCore import QThread, pyqtSignal


class PathCheckWorker(QThread):
    each_result_signal = pyqtSignal(list)

    def __init__(self, idx, buf):
        super().__init__()
        self.idx = idx
        self.buf = buf
        self.to_be_terminated = False

    def run(self):
        for line in self.buf:
            if self.to_be_terminated:
                break
            path = line.strip().replace("\n", "").strip()
            is_existed = os.path.exists(path)
            self.each_result_signal.emit([self.idx, is_existed, path])

    def to_terminate(self):
        self.to_be_terminated = True
