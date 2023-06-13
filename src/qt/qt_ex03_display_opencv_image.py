import cv2
import numpy as np
import sys

from PySide2.QtWidgets import *
from PySide2.QtGui import *


class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle('display opencv image')

        self.imageLabel = QLabel()
        self.imageLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setPixmap(QPixmap())

        openButton = QPushButton('Open', self)
        openButton.clicked.connect(self.open)

        pencilSketchButton = QPushButton('Pencil', self)
        pencilSketchButton.clicked.connect(self.toPencilSketch)

        originalButton = QPushButton('Original', self)
        originalButton.clicked.connect(self.toOriginal)

        buttonBox = QWidget(self)
        buttonBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonBox.resize(500, 200)


        self.groupBox = QGroupBox('', buttonBox)
        buttonSubLayout = QHBoxLayout(self.groupBox)
        buttonSubLayout.addWidget(pencilSketchButton)
        buttonSubLayout.addWidget(originalButton)
        self.groupBox.setEnabled(False)

        buttonLayout = QHBoxLayout(buttonBox)
        buttonLayout.addWidget(openButton)
        buttonLayout.addWidget(self.groupBox)
        
        # [ImageLabel]
        # [Open] | [Pencil]

        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        layout.addWidget(buttonBox)

        self.setLayout(layout)
        self.resize(500, 500)

    def open(self):
        fileName,_ = QFileDialog.getOpenFileName(self, '이미지파일열기', '.', 'Images (*.png *.jpg *.jpeg)')
        
        # "", '', None
        if not fileName:
            return
        
        self.loadedFilePath = fileName
        self.load(fileName)
            

    def load(self, fileName):
        # opencv를 통해 이미지를 열어준다

        img = cv2.imread(fileName)
        # None 자료형은 is 비교하는것이 가장 안전 (is == 자료형 비교)
        if img is None:
            return

        # 색상구조 변환 (BRG -> RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h,w,c = img.shape
        # OpenCV Mat과 QImage의 구조적 차이로 3번째 인수에 bytesPerLine 명시가 필요
        qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.imageLabel.setPixmap(pixmap)
        self.groupBox.setEnabled(True)

    def toOriginal(self):
        self.load(self.loadedFilePath)

    def toPencilSketch(self):

        # 이미지의 경로를 가져와 opencv로 열고 효과를 준다음 이미지 재표시
        img = cv2.imread(self.loadedFilePath)
        # None 자료형은 is 비교하는것이 가장 안전 (is == 자료형 비교)
        if img is None:
            return

        # 블러
        img = cv2.GaussianBlur(img, ksize=(9, 9), sigmaX=0)
        # 연필효과를 주는 함수
        img,_ = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.05, shade_factor=0.015)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        h,w,c = img.shape
        # OpenCV Mat과 QImage의 구조적 차이로 3번째 인수에 bytesPerLine 명시가 필요
        qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.imageLabel.setPixmap(pixmap)

        pass

if __name__ == '__main__':

    app = QApplication(sys.argv)

    # 최상위 위젯(윈도우) 생성 및 표시

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec_()