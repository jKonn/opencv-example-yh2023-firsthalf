from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import sys

# pip install pyserial
import serial


class Worker(QThread):
    readText = Signal(str)
    working = True
    def run(self):
        while self.working:
            if ser.readable():
                result = ser.readline()
                result = result.decode()
                result = result.replace('\r\n', '')
                # print(result, end='')
                # print(result)

                self.readText.emit(result)
                self.msleep(300)
        ser.close()

    def stop(self):
        self.working = False
        self.quit()
        self.wait(5000)



class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.inputLineEdit = QLineEdit(self)
        self.sendButton = QPushButton('&Send', self)
        self.sendButton.clicked.connect(self.sendText)

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.inputLineEdit)
        inputLayout.addWidget(self.sendButton)

        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addLayout(inputLayout)
        layout.addWidget(self.textEdit)

        self.worker = Worker()
        self.worker.start()
        self.worker.readText.connect(self.printText)

        self.resize(500,500)



    def printText(self, read):
        self.textEdit.setText(self.textEdit.toPlainText() + read)


    def sendText(self):
        inputText = self.inputLineEdit.text()
        print('inputText:', inputText)

        # 시리얼통신 (serial) => 직렬화 (데이터를 직선상으로 나열)
        # Rx/Tx (받기/보내기) -> Tx/Rx
        # 보드레이트 baudrate
        # 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200
        # TODO 시리얼통신을 이용해 문자열을 전송
        ser.write(inputText.encode())
        self.inputLineEdit.setText('')

        pass

PORT = '/dev/ttyUSB0'
def prepare():

    global ser

    # 시리얼 포트 연결
    # 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200
    ser = serial.serial_for_url(PORT, baudrate=9600, timeout=1)
    pass

if __name__ == '__main__':

    prepare()
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
    window.worker.stop()