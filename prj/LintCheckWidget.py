import os
import time
from functools import partial

from PyQt5.QtCore import QProcess, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QPushButton, QMessageBox


class LintCheckWin(QWidget):
    m_list_signal = pyqtSignal(list)
    close_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.p = None
        self.module_value = None
        self.module_key = None
        self.report_value = None
        self.report_key = None
        self.check_value = None
        self.check_key = None
        self.setMinimumWidth(300)
        self.setMinimumHeight(500)
        self.project_label_value = None
        self.project_label_key = None
        self.sub_modules = None
        self.modules = None
        self.report_path = None
        self.check_path = None
        self.project_name = None
        self.top_widget = None
        self.bottom_widget = None
        self.message_box = None
        self.sub_module_btn_grp = []
        self.review_btn_grp = []
        self.extract_log_processes = None
        self.final_report_path = None
        self.m_list_signal.connect(self.extract_log)
        self.parsing_config()
        self.init_ui()
        self.start_process()

    def init_ui(self):
        self.project_label_key = QLabel("Project")
        self.project_label_value = QLabel(self.project_name)
        self.check_key = QLabel("Check Path")
        self.check_value = QLabel(self.check_path)
        self.report_key = QLabel("Report Path")
        self.report_value = QLabel(self.report_path)
        self.module_key = QLabel("Modules")
        self.module_value = QLabel(self.modules)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.project_label_key, 0, 0)
        grid_layout.addWidget(self.project_label_value, 0, 1)
        grid_layout.addWidget(self.check_key, 1, 0)
        grid_layout.addWidget(self.check_value, 1, 1)
        grid_layout.addWidget(self.report_key, 2, 0)
        grid_layout.addWidget(self.report_value, 2, 1)
        grid_layout.addWidget(self.module_key, 3, 0)
        grid_layout.addWidget(self.module_value, 3, 1)
        self.top_widget = QWidget()
        self.top_widget.setLayout(grid_layout)

        self.message_box = QLabel("Ready")
        grid_layout_1 = QGridLayout()
        row = 0
        for module in self.sub_modules:
            module_btn = QPushButton(module)
            module_btn.clicked.connect(partial(self.open_sub_module_log, idx=row))
            review_btn = QPushButton("Review")
            module_btn.setDisabled(True)
            review_btn.setDisabled(True)
            self.sub_module_btn_grp.append(module_btn)
            self.review_btn_grp.append(review_btn)
            grid_layout_1.addWidget(module_btn, row, 0)
            grid_layout_1.addWidget(review_btn, row, 1)
            row += 1
        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(grid_layout_1)
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.top_widget)
        v_layout.addWidget(self.message_box)
        v_layout.addWidget(self.bottom_widget)
        self.setLayout(v_layout)

    def parsing_config(self):
        with open("config/lint_check_config", "r") as _f:
            lines = _f.readlines()
            for line in lines:
                if line.startswith("project"):
                    self.project_name = line.split("=")[-1].strip().replace("\n", "").strip()
                elif line.startswith("check_path"):
                    self.check_path = line.split("=")[-1].strip().replace("\n", "").strip()
                elif line.startswith("report_path"):
                    self.report_path = line.split("=")[-1].strip().replace("\n", "").strip()
                elif line.startswith("modules"):
                    self.modules = line.split("=")[-1].strip().replace("\n", "").strip()
                elif line.startswith("sub_modules"):
                    self.sub_modules = line.split("=")[-1].strip().split(",")
                    self.extract_log_processes = [None] * len(self.sub_modules)

    def start_process(self):
        if self.p is None:  # No process running.
            print("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            cmd = f'ls {self.report_path} |grep {self.modules}'
            self.p.start('bash', ['-c', cmd])

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        print(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        if stdout.count('\n') == 1:
            self.final_report_path = os.path.join(self.report_path, stdout.strip().replace('\n', '').strip())
            print(self.final_report_path)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        print(f"State changed: {state_name}")

    def process_finished(self):
        print("Process finished.")
        self.p = None
        idx = 0
        for m in self.sub_modules:
            m_list = [m, self.final_report_path, idx]
            idx += 1
            self.m_list_signal.emit(m_list)

    @pyqtSlot(list)
    def extract_log(self, l):
        p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
        self.extract_log_processes[l[2]] = p
        # p.readyReadStandardOutput.connect(self.handle_stdout)
        # p.readyReadStandardError.connect(self.handle_stderr)
        # p.stateChanged.connect(self.handle_state)
        p.finished.connect(partial(self.extract_log_finished, idx=l[2]))  # Clean up once complete.
        result_path = os.path.join(self.report_path, f"{l[0]}.log")
        cmd = f'grep {l[0]} {l[1]} >> {result_path}'
        p.start('bash', ['-c', cmd])

    def extract_log_finished(self, idx):
        print("Process finished.")
        self.extract_log_processes[idx] = None
        self.sub_module_btn_grp[idx].setDisabled(False)
        self.review_btn_grp[idx].setDisabled(False)

    def open_sub_module_log(self, idx):
        result_path = os.path.join(self.report_path, f"{self.sub_modules[idx]}.log")
        cmd = f"mvim {result_path}"
        os.system(cmd)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the Lint Check Window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for p in self.extract_log_processes:
                print(p.state())
            time.sleep(10)
            event.accept()
            self.close_signal.emit("lint")
        else:
            event.ignore()
