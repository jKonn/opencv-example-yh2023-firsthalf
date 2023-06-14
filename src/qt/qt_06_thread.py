import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class Worker(QThread):

    def run(self):
        while True:
            print("안녕하세요")
            self.sleep(1) #초단위
    


class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.worker = Worker()
        self.worker.start()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()