import time

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Worker(QObject):
    progress = pyqtSignal(int)
    completed = pyqtSignal(int)

    @pyqtSlot(int)
    def do_work(self, n):
        for i in range(1, n + 1):
            time.sleep(1)
            self.progress.emit(i)

        self.completed.emit(i)

