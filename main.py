import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from prj.MainWidget import MainWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setFixedSize(800,600)
    main_widget = MainWidget()
    window.setCentralWidget(main_widget)
    window.show()
    app.exec()