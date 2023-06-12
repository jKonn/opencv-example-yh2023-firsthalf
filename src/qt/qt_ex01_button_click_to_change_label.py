from PySide2.QtWidgets import *

import sys


names = (
    '이재권',
    'jKon',
    '권',
    '콘',
    'kon',
    '재권',
)

# names = [
#     '이재권',
#     'jKon',
#     '권',
#     '콘',
#     'kon',
#     '재권',
# ]

nameIndex = 0

def onClick():
    global nameIndex

    # 인덱스가 최대값을 벗어나면

    # 1.처음부터 다시 반복
    # nameIndex = nameIndex + 1
    # if nameIndex >= len(names):
    #     nameIndex = 0

    # 0 % 6 = 0, 1 % 6 = 1.... , 6 % 6 = 0
    nameIndex = (nameIndex + 1) % len(names)

    # 2.최대값에 고정
    # nameIndex = nameIndex + 1
    # if nameIndex >= len(names):
    #     nameIndex = len(names)-1

    # nameIndex = min(nameIndex + 1, len(names)-1)

    print('nameIndex:', nameIndex)

    # global label
    # label = QLabel()
    label.setText(names[nameIndex])


if __name__ == '__main__':

    global label
    app = QApplication(sys.argv)

    # 메인윈도우
    window = QWidget()
    window.resize(500,500)
    window.move(500, 500)
    window.setWindowTitle('call myname')

    # 메인안에 QLabel + QButton
    label = QLabel(names[nameIndex], window)
    button = QPushButton('확인', window)
    # QButton 클릭시 동작할 함수
    button.clicked.connect(onClick)

    layout = QVBoxLayout(window)
    layout.addWidget(label)
    layout.addWidget(button)

    window.show()

    app.exec_()