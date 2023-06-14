import cv2
import numpy as np
import time

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import sys


class Worker(QThread):

    capture = Signal(QImage)

    def run(self):
        # OpenCV 로 읽어온 VideoCapture의 Frame을 외부로 전달

        self.cap = cv2.VideoCapture(0)
        if (self.cap.isOpened()):

            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break

                # 색상구조 변환 (BRG -> RGB)
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h,w,c = img.shape
                qImg = QImage(img.data, w, h, w * c, QImage.Format_RGB888)
                self.capture.emit(qImg)

                # pixmap = QPixmap.fromImage(qImg)
                # self.imageLabel.setPixmap(pixmap)

                self.msleep(25)
        
        self.cap.release()


class MainWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Cam viewer')
        
        # QLabel 생성 및 기타 설정 (이미지 표시를 위한 기본 설정)
        # 기본 빈이미지를 표시
        self.imageLabel = QLabel()
        self.imageLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setPixmap(QPixmap())

        self.button = QPushButton('&cam', self)
        self.button.clicked.connect(self.onClicked)

        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        self.resize(QApplication.primaryScreen().availableSize()*2/5)

    def onClicked(self):
        self.displayCam()

    def showFrame(self, frame:QImage):
        pixmap = QPixmap.fromImage(frame)
        self.imageLabel.setPixmap(pixmap)

    def displayCam(self):

        # 비디오를 읽어오는 쓰레드 동작
        self.worker = Worker()
        self.worker.capture.connect(self.showFrame)
        self.worker.start()

        # cap = cv2.VideoCapture(0)
        # if (cap.isOpened()):

        #     while True:
        #         ret, frame = cap.read()

        #         if not ret:
        #             break

        #         # 색상구조 변환 (BRG -> RGB)
        #         img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         h,w,c = img.shape
        #         qImg = QImage(img.data, w, h, w * c, QImage.Format_RGB888)
        #         pixmap = QPixmap.fromImage(qImg)

        #         self.imageLabel.setPixmap(pixmap)

        #         # time.sleep(0.25)

        #         if (cv2.waitKey(1) >= 0):
        #             break

        # cap.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
