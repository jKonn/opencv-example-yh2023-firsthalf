import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class Worker(QThread):

    # timeout = pyqtSignal(int) #PyQt5, QtCore 안에 정의
    timeout = Signal(int) #PySide2, QtCore 안에 정의
    
    def __init__(self):
        super().__init__()
        self.num = 0

    def run(self):
        while True:
            
            # 방출, 값을 전달, 내보내기
            # 해당 시그널(signal)에 연결된(connect) 함수가 있다면 해당 함수에 값을 전달해서 호출함
            self.timeout.emit(self.num)
            self.num += 1
            self.sleep(1)


class MainWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.worker = Worker()
        self.worker.start()
        self.worker.timeout.connect(self.timeout)

        self.edit = QLineEdit(self)
        self.edit.setReadOnly(True)
        self.edit.move(10,10)

    @Slot(int)
    def timeout(self, num):
        self.edit.setText(str(num))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()