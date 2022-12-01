import time
import os

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Worker(QObject):
    progress = pyqtSignal(bool)
    completed = pyqtSignal(int)

    def _process(self, path):
        return os.path.exists(path)

    def __init__(self, buf):
        super().__init__()
        self.buf = buf

    @pyqtSlot()
    def do_work(self):
        s = time.time()
        for line in self.buf:
            res = self._process(line.replace('\n', ''))
            self.progress.emit(res)
        print(f"Elasped: {time.time()-s}")

        # self.completed.emit(i)
