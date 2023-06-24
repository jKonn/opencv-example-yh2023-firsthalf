from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import sys
import serial


notes = [
    ('도', '1'),
    ('레', '2'),
    ('미', '3'),
    ('파', '4'),
    ('솔', '5'),
    ('라', '6'),
    ('시', '7'),
    ('도', '8'),
]

NOTE_NAME = 0
NOTE_VALUE = 1

class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QHBoxLayout(self)

        # 도~도 8음계 버튼
        for note in notes:
            noteButton = QPushButton(note[NOTE_NAME], self)
            noteButton.setObjectName(note[NOTE_VALUE])
            noteButton.clicked.connect(self.onClickMelody)
            layout.addWidget(noteButton)

        self.resize(500, 500)

    def onClickMelody(self):

        sender = self.sender()
        # print('sender: ', sender)
        # msg = sender.text()
        msg = sender.objectName()
        print('sender msg: ', msg)

        self.sendMsg(msg)
        pass

    def sendMsg(self, msg:str):
        # 시리얼통신 메세지 전달

        # ser.write(msg.encode())
        pass
    

PORT = '/dev/ttyUSB0'

if __name__ == '__main__':

    # ser = serial.serial_for_url(PORT, baudrate=9600, timeout=1)

    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec_()