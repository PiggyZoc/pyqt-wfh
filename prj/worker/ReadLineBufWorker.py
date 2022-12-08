import os

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread


class ReadLineBufWorker(QThread):
    buf_idx_list_signal = pyqtSignal(list)

    def __init__(self, idx, filename):
        super().__init__()
        self.idx = idx
        self.filename = filename

    def run(self):
        file_size = os.path.getsize(self.filename)
        buf_size = file_size // 3
        big_file = open(self.filename, "r")
        temp_lines = big_file.readlines(buf_size)
        results = []
        total = 0
        while temp_lines:
            results.append(temp_lines)
            total += len(temp_lines)
            temp_lines = big_file.readlines(buf_size)
        self.buf_idx_list_signal.emit([self.idx, total, results])
