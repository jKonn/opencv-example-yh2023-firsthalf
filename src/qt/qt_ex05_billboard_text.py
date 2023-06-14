# 왼쪽으로 흐르는 텍스트 (빌보드)
# 초기 값에서 왼쪽으로 한글자씩 이동하며 흐른다
# **왼쪽으로 벗어난 텍스트는 가장 오른쪽에 다시 나옴
# 프로그램이 종료될때까지 계속 반복
# hello
# elloh
# llohe
# lohel
# ohell
# hello

# import os
# #linux & mac
# os.system('clear')
# #windows
# os.system('cls')




from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import sys

class Worker(QThread):

    printText = Signal(str)

    def __init__(self, text:str):
        super().__init__()

        self.words = [c for c in text]
        # for c in text:
        #     self.words.append(c)

        self.textLength = len(self.words)
        self.working = True

        # print('self.words: ', self.words)

    def run(self):

        while self.working:

            resultStr = ''.join(self.words)
            # print('result: ', resultStr)

            self.printText.emit(resultStr)

            # 스왑하면서 전체가 한칸씩 이동
            for i in range(0, self.textLength-1):

                next_i = i+1
                val1 = self.words[i]
                val2 = self.words[next_i]

                # 스왑
                self.words[i] = val2
                self.words[next_i] = val1
            
            self.sleep(1)

    def stop(self):
        self.working = False
        self.quit()
        self.wait(5000) #5000ms = 5s

    def pause(self):
        self.working = False
        

class MainWindow(QWidget): 

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.playing = False

        self.textLabel = QLabel(self)
        self.textLineEdit = QLineEdit(self)

        self.playButton = QPushButton('&Play', self)
        self.playButton.clicked.connect(self.onClickPlayToggle)
        self.stopButton = QPushButton('&Stop', self)
        self.stopButton.clicked.connect(self.onClickStop)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addWidget(self.stopButton)

        layout = QVBoxLayout()
        layout.addWidget(self.textLineEdit)
        layout.addWidget(self.textLabel)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def onClickPlayToggle(self):

        if self.playing:
            self.worker.pause()

        else:
            inputText = self.textLineEdit.text()
            if len(inputText) < 2:
                return

            self.worker = Worker(inputText)
            # self.worker.printText.connect(self.textLabel.setText)
            self.worker.printText.connect(self.onPrintText)
            self.worker.start()

            self.textLineEdit.setEnabled(False)

        self.playing = not self.playing

    def onClickStop(self):
        self.playing = False
        self.worker.stop()
        self.textLineEdit.setEnabled(True)
        self.textLabel.setText('')


    def onPrintText(self, text):
        self.textLabel.setText(text)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
