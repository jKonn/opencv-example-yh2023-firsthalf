from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import sys
import serial

class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # 도~도 8음계 버튼
        self.noteButton1 = QPushButton(self)
        self.noteButton2 = QPushButton(self)
        self.noteButton3 = QPushButton(self)
        self.noteButton4 = QPushButton(self)
        self.noteButton5 = QPushButton(self)
        self.noteButton6 = QPushButton(self)
        self.noteButton7 = QPushButton(self)
        self.noteButton8 = QPushButton(self)

        layout = QHBoxLayout(self)
        layout.addWidget(self.noteButton1)
        layout.addWidget(self.noteButton2)
        layout.addWidget(self.noteButton3)
        layout.addWidget(self.noteButton4)
        layout.addWidget(self.noteButton5)
        layout.addWidget(self.noteButton6)
        layout.addWidget(self.noteButton7)
        layout.addWidget(self.noteButton8)

        self.resize(500, 500)
        pass

PORT = '/dev/ttyUSB0'

if __name__ == '__main__':

    ser = serial.serial_for_url(PORT, baudrate=9600, timeout=1)

    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec_()