from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import sys
import serial

class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # 도~도 8음계 버튼
        self.noteButton1 = QPushButton('도', self) #도
        self.noteButton2 = QPushButton('레', self) #레
        self.noteButton3 = QPushButton('미', self) #미
        self.noteButton4 = QPushButton('파', self) #파
        self.noteButton5 = QPushButton('솔', self) #솔
        self.noteButton6 = QPushButton('라', self) #라
        self.noteButton7 = QPushButton('시', self) #시
        self.noteButton8 = QPushButton('도(+1)', self) #도

        layout = QHBoxLayout(self)
        layout.addWidget(self.noteButton1)
        layout.addWidget(self.noteButton2)
        layout.addWidget(self.noteButton3)
        layout.addWidget(self.noteButton4)
        layout.addWidget(self.noteButton5)
        layout.addWidget(self.noteButton6)
        layout.addWidget(self.noteButton7)
        layout.addWidget(self.noteButton8)

        self.noteButton1.clicked.connect(self.onClickMelody1)
        self.noteButton2.clicked.connect(self.onClickMelody2)
        self.noteButton3.clicked.connect(self.onClickMelody3)
        self.noteButton4.clicked.connect(self.onClickMelody4)
        self.noteButton5.clicked.connect(self.onClickMelody5)
        self.noteButton6.clicked.connect(self.onClickMelody6)
        self.noteButton7.clicked.connect(self.onClickMelody7)
        self.noteButton8.clicked.connect(self.onClickMelody8)

        self.resize(500, 500)


    def onClickMelody1(self):

        self.sendMsg('1')
        pass

    def onClickMelody2(self):

        self.sendMsg('2')
        pass

    def onClickMelody3(self):

        self.sendMsg('3')
        pass

    def onClickMelody4(self):

        self.sendMsg('4')
        pass

    def onClickMelody5(self):

        self.sendMsg('5')
        pass

    def onClickMelody6(self):

        self.sendMsg('6')
        pass

    def onClickMelody7(self):

        self.sendMsg('7')
        pass

    def onClickMelody8(self):

        self.sendMsg('8')
        pass

    def sendMsg(self, msg:str):
        # 시리얼통신 메세지 전달

        ser.write(msg.encode())
        pass
    

PORT = '/dev/ttyUSB0'

if __name__ == '__main__':

    ser = serial.serial_for_url(PORT, baudrate=9600, timeout=1)

    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec_()