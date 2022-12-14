import os.path
import time
from functools import partial
from PyQt5.QtCore import pyqtSignal, QProcess, pyqtSlot
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox

from prj.worker.PathCheckWorker import PathCheckWorker
from prj.worker.ReadLineBufWorker import ReadLineBufWorker


def open_file(path):
    os.system(f"mvim {path}")


class SocAsyncListWin(QWidget):
    close_signal = pyqtSignal(str)
    btn_style = "height:26px;border-radius:13px;background-color:rgb(255, 239, 0);font-weight:bold;"
    btn_red_style = "height:26px;border-radius:13px;background-color:rgb(220,20,60);font-weight:bold;"
    btn_green_style = "height:26px;border-radius:13px;background-color:rgb(153,230,77);font-weight:bold;"
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.all_btn = None
        self.folder = None
        self.module_lst = None
        self.env_value = None
        self.env_key = None
        self.p = None
        self.lst_file_list = None
        self.line_buf_lst = None
        self.line_buf_total = None
        self.progress_lst = None
        self.read_buf_threads = None
        self.worker_factory = []
        self.lst_num = None
        self.m_btn_grp = []
        self.m_btn_lst_grp = []
        self.log_btn_grp = []
        self.lst_processes = None
        self.out_file_ptrs = None
        self._lock = False
        self.parsing_config()
        self.init_ui()
        self.activate_btns()

    def parsing_config(self):
        with open("config/soc_async_list_config", "r") as _f:
            lines = _f.readlines()
            for l in lines:
                if l.startswith("env"):
                    self.env_key = l.split()[-1].strip().replace("\n", "").split("=")[0].strip()
                    self.env_value = l.split()[-1].strip().replace("\n", "").split("=")[-1].strip()
                elif l.startswith("modules"):
                    self.module_lst = l.split("=")[-1].strip().replace("\n", "").split(",")
                    self.lst_processes = [None] * len(self.module_lst)
                    self.lst_num = [0] * len(self.module_lst)
                    self.lst_file_list = [None] * len(self.module_lst)
                    self.line_buf_lst = [None] * len(self.module_lst)
                    self.line_buf_total = [None] * len(self.module_lst)
                    self.read_buf_threads = [None] * len(self.module_lst)
                    self.progress_lst = [0] * len(self.module_lst)
                    self.out_file_ptrs = [None] * len(self.module_lst)
                elif l.startswith("folder"):
                    self.folder = l.split("=")[-1].strip().replace("\n", "").strip()
                else:
                    pass

    def init_ui(self):
        grid_layout = QGridLayout()
        self.all_btn = QPushButton("soc.async.lst")
        self.all_btn.setDisabled(True)
        grid_layout.addWidget(self.all_btn, 0, 0)
        row = 1
        for e in self.module_lst:
            m_btn = QPushButton(e)
            m_btn_lst = QPushButton(f"{e}_file_list")
            m_log_btn = QPushButton("Log")
            m_btn.setDisabled(True)
            m_btn_lst.setDisabled(True)
            m_log_btn.setDisabled(True)
            self.m_btn_grp.append(m_btn)
            self.m_btn_lst_grp.append(m_btn_lst)
            self.log_btn_grp.append(m_log_btn)
            grid_layout.addWidget(m_btn, row, 0)
            grid_layout.addWidget(m_btn_lst, row, 1)
            grid_layout.addWidget(m_log_btn, row, 2)
            row += 1
        self.setLayout(grid_layout)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the SOC ASYNC LIST Window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.kill_processes()
            time.sleep(0.1)
            for worker in self.worker_factory:
                if worker is not None:
                    worker.to_terminate()
            time.sleep(0.1)
            self.close_signal.emit("soc")
        else:
            event.ignore()

    def activate_btns(self):
        idx = 0
        for m in self.module_lst:
            filename = os.path.join(self.folder, f".{m}")
            with open(filename, "w+") as out:
                with open(os.path.join(self.folder, m), "r") as _f:
                    lines = _f.readlines()
                    for line in lines:
                        if line.startswith("-f"):
                            sub_line = line.split()[-1].strip().replace("\n", "").replace(self.env_key, "").strip()
                            if sub_line.startswith('/'):
                                sub_line = sub_line.removeprefix('/')
                            new_line = os.path.join(self.env_value, sub_line)
                            print(new_line, file=out)
            self.m_btn_grp[idx].clicked.connect(partial(open_file, path=filename))
            self.m_btn_grp[idx].setDisabled(False)
            self.m_btn_grp[idx].setStyleSheet(self.btn_style)
            self.activate_lst_btns(filename, idx)
            idx += 1

    def activate_lst_btns(self, filename, idx):
        bash_file = os.path.join(self.folder, f".{idx}")
        if os.path.exists(bash_file):
            os.remove(bash_file)
        result_file = os.path.join(self.folder, f".{idx}_lst_result")
        if os.path.exists(result_file):
            os.remove(result_file)
        with open(bash_file, "w+") as _bash:
            print("#!/bin/bash", file=_bash)
            with open(filename, "r") as in_file:
                lines = in_file.readlines()
                new_value = self.env_value.replace("/", r"\/")
                for line in lines:
                    line = line.strip().replace("\n", "").strip()
                    cmd = f"sed 's/{self.env_key}/{new_value}/g' {line} >> {result_file}"
                    print(cmd, file=_bash)
        self.m_btn_lst_grp[idx].clicked.connect(partial(open_file, path=result_file))
        p = QProcess()
        self.lst_processes[idx] = p
        self.lst_file_list[idx] = result_file
        p.finished.connect(partial(self.trigger_lst_btn, idx=idx))
        p.start(f"bash {bash_file}")

    def trigger_lst_btn(self, idx):
        self.m_btn_lst_grp[idx].setDisabled(False)
        self.m_btn_lst_grp[idx].setStyleSheet(self.btn_style)
        self.lst_num[idx] = 1
        self.lst_processes[idx] = None

        worker = ReadLineBufWorker(idx, self.lst_file_list[idx])
        worker.buf_idx_list_signal.connect(self.on_read_buf_signal_received)
        self.read_buf_threads[idx] = worker
        worker.start()
        if len(self.lst_num) == sum(self.lst_num):
            all_file_lst = os.path.join(self.folder, ".final_result")
            if os.path.exists(all_file_lst):
                os.remove(all_file_lst)
            cmd = "cat\40"
            self.all_btn.clicked.connect(partial(open_file, path=all_file_lst))
            for each in self.lst_file_list:
                cmd += f"{each}\40"
            cmd += f">\40{all_file_lst}"
            if self.p is None:
                self.p = QProcess()
                self.p.finished.connect(self.trigger_all_btn)
                self.p.start("bash", ["-c", cmd])

    def trigger_all_btn(self):
        self.all_btn.setDisabled(False)
        self.all_btn.setStyleSheet(self.btn_style)
        self.p = None

    @pyqtSlot(list)
    def on_read_buf_signal_received(self, m_list):
        idx = m_list[0]
        total = m_list[1]
        line_buf = m_list[2]
        self.line_buf_lst[idx] = line_buf
        self.line_buf_total[idx] = total
        log_result_file = os.path.join(self.folder, f".{idx}.log")
        if os.path.exists(log_result_file):
            os.remove(log_result_file)
        file_ptr = open(log_result_file, "a")
        self.out_file_ptrs[idx] = file_ptr
        for each_buf in self.line_buf_lst[idx]:
            worker = PathCheckWorker(idx, each_buf)
            worker.each_result_signal.connect(self.update_progress)
            self.worker_factory.append(worker)
            worker.start()

    @pyqtSlot(list)
    def update_progress(self, m_list):
        while self._lock:
            time.sleep(0.2)
        self._lock = True
        idx = m_list[0]
        self.progress_lst[idx] += 1
        is_existed = m_list[1]
        path = m_list[2]
        if not is_existed:
            print(f"{path} NOT EXIST!", file=self.out_file_ptrs[idx])
        progress = 100 * self.progress_lst[idx] / self.line_buf_total[idx]
        percent = f'%.0f%%' % progress
        self.log_btn_grp[idx].setText(percent)
        self._lock = False
        if progress == 100:
            time.sleep(0.2)
            self.out_file_ptrs[idx].close()
            self.on_completion(idx)

    def on_completion(self, idx):
        if os.path.getsize(os.path.join(self.folder, f".{idx}.log")) == 0:
            self.log_btn_grp[idx].setText("Passed")
            self.log_btn_grp[idx].setStyleSheet(self.btn_green_style)
            return
        self.log_btn_grp[idx].setText("View Log")
        self.log_btn_grp[idx].clicked.connect(partial(open_file, path=os.path.join(self.folder, f".{idx}.log")))
        self.log_btn_grp[idx].setStyleSheet(self.btn_red_style)
        self.log_btn_grp[idx].setDisabled(False)

    def kill_processes(self):
        for p in self.lst_processes:
            if p is not None:
                p.kill()
        if self.p is not None:
            self.p.kill()
