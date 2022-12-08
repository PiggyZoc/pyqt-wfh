import os.path
from datetime import datetime

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QRadioButton, QHBoxLayout, QTextEdit, QPushButton, QVBoxLayout, QTextBrowser, \
    QMessageBox


class RemarkWin(QWidget):
    btn_style = "height:26px;border-radius:13px;background-color:rgb(255, 239, 0);font-weight:bold;"
    close_signal = pyqtSignal(int)
    save_signal = pyqtSignal(list)

    def __init__(self, idx, review_path):
        super().__init__()
        self.text_browser = None
        self.left_widget = None
        self.bottom_widget = None
        self.cancel_btn = None
        self.save_and_exit_btn = None
        self.text_edit = None
        self.top_widget = None
        self.go_btn = None
        self.pend_btn = None
        self.idx = idx
        self.review_path = review_path
        self.choice = "PEND"
        self.init_ui()

    def init_ui(self):
        self.pend_btn = QRadioButton("PEND")
        self.pend_btn.setChecked(True)
        self.go_btn = QRadioButton("GO")
        self.pend_btn.toggled.connect(self.on_radio_btn_checked)
        self.go_btn.toggled.connect(self.on_radio_btn_checked)
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.pend_btn)
        top_layout.addWidget(self.go_btn)
        self.top_widget = QWidget()
        self.top_widget.setLayout(top_layout)

        self.text_edit = QTextEdit()

        self.save_and_exit_btn = QPushButton("Save&&Exit")
        self.save_and_exit_btn.setStyleSheet(self.btn_style)
        self.save_and_exit_btn.clicked.connect(self.on_save_btn_clicked)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(self.btn_style)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.save_and_exit_btn)
        bottom_layout.addWidget(self.cancel_btn)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(bottom_layout)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.top_widget, 1)
        left_layout.addWidget(self.text_edit, 4)
        left_layout.addWidget(self.bottom_widget, 1)
        self.left_widget = QWidget()
        self.left_widget.setLayout(left_layout)

        self.text_browser = QTextBrowser()

        if os.path.exists(self.review_path):
            with open(self.review_path, "r") as _f:
                content = _f.read()
                self.text_browser.setPlainText(content)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_widget)
        main_layout.addWidget(self.text_browser)

        self.setLayout(main_layout)

    def on_radio_btn_checked(self):
        if self.pend_btn.isChecked():
            self.choice = "PEND"
        elif self.go_btn.isChecked():
            self.choice = "GO"
        else:
            pass

    def on_save_btn_clicked(self):
        remark = self.text_edit.toPlainText().strip()
        if remark == "":
            QMessageBox.information(self, 'Message',
                                            'Remark is Empty! Unable to save!',
                                            QMessageBox.Ok )
            return
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y %H:%M:%S")
        comments = f"明 with {self.choice} \n {remark} \n {date_time}"
        with open(self.review_path, "a") as _f:
            print(comments, file=_f)
        self.save_signal.emit([self.idx, self.choice])