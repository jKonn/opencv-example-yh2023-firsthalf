# [Map Spec]
# 지정된 맵은 9x9의 격자구조
# S == 시작지점, F == 도착지점, 
# o == 갈 수 있는길, x == 갈 수 없는길, 
# P == 플레이어
# 해당 심볼로 작성된 맵을 파싱하여 메모리에 올려 좌표로 및 표시로 사용가능 하도록 구조화
# 맵을 파일로 부터 읽어서 파싱
# (맵 데이터를 구조화 하는것이 관건!, 메모리에 미리 올려놓고 사용해도 무관!)

# [Play Rule]
# 1.플레이어는 처음시작시 S 위치에서 시작하고
# 2.현 플레이어 위치에서 갈 수 있는 방향을 지문으로 표시
#   2-1.지문예시: 
#      1) 북쪽으로 이동
#      2) 동쪽으로 이동
#      3) 남쪽으로 이동
#      4) 서쪽으로 이동
# 3.플레이어가 선택한 지문의 방향으로 P를 이동시킴 (사용자의 입력을 기다리고 있음)
#   3-1.선택한 방향이 유효하다면 플레이어의 현재위치를 이동위치로 변경
#   3-2.선택한 방향이 비유효하다면 플레이어의 현재위치는 변동없음
#     (진행이 불가하다는 메세지를 잠깐 표시하면 더좋음)
# 4.다시 2번부터 반복

# 9x9 한줄은 줄내림(\n)으로 구분되어있고, 한줄 안에 각 열은 띄어쓰기(' ')로 구분되어있음
# 각 tile은 "o" 와 "x" 로 구분되어있고, "x"는 갈 수 없는 길이다.
# 시작지점은 "S", 도착지점은 "F", 플레이어의 위치는 "P"로 표시
# 좌표화 필요 (2차원, 두개의 축이 필요, x,y)
# o x o x x x x o F 
# o o o x x o o o x 
# o x o x o o x o x 
# o o o o o x x o o 
# x x x x o o x x x 
# o o o o x o o o o 
# x o x o o o x o x 
# o o o o x o o o x 
# S x x o o x x o x

# x x x x x x x x x x x
# x o x o x x x x o F x
# x o o o x x o o o x x 
# x o x o x o o x o x x
# x o o o o o x x o o x
# x x x x x o o x x x x 
# x o o o o x o o o o x 
# x x o x o o o x o x x 
# x o o o o x o o o x x 
# x S x x o o x x o x x
# x x x x x x x x x x x


# mapData = [
#     ['o','x','o','x','x','x','x','o','F'],
#     ['o','x','o','x','x','x','x','o','F'],
#     ['o','x','o','x','x','x','x','o','F'],
#     ['o','x','o','x','x','x','x','o','F'],
#     ['o','x','o','x','x','x','x','o','F'],
#     ['o','x','o','x','x','x','x','o','F'],
#     ['o','x','o','x','x','x','x','o','F'],
#     ['o','x','o','x','x','x','x','o','F'],
#     ['o','x','o','x','x','x','x','o','F'],
# ]

# row,col
# mapData[y][x]


from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import sys
import os

DIRECTION_DATAS = [
    # 북
    {
        'tag': 'u',
        'label': '↑',
        'offset': (-1,0),
        'position': (0,1),
    },
    # 남
    {
        'tag': 'd',
        'label': '↓',
        'offset': (1,0),
        'position': (1,1),
    },
    # 서
    {
        'tag': 'l',
        'label': '←',
        'offset': (0,-1),
        'position': (1,0),
    },
    # 동
    {
        'tag': 'r',
        'label': '→',
        'offset': (0,1),
        'position': (1,2),
    }
]

KEY_MAP = {
    Qt.Key_W:0,
    Qt.Key_S:1,
    Qt.Key_A:2,
    Qt.Key_D:3,

    Qt.Key_Up:0,
    Qt.Key_Down:1,
    Qt.Key_Left:2,
    Qt.Key_Right:3,
}


class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.mapData = []
        self.startPos = ()
        self.finishPos = ()
        self.playerPos = []
        self.maxRow = -1
        self.maxCol = -1

        # QLineEdit #한줄로만
        # QLabel #한줄로만
        # QTextEdit #다수의 줄을 지원

        self.mapView = QTextEdit()
        self.mapView.setReadOnly(True)
        self.mapView.setFont(QFont('monospace', 20))
        self.mapView.setAlignment(Qt.AlignCenter)

        # https://symbl.cc/en/collections/arrow-symbols/

        #|    | 위   |    |
        #|  < | 아래 | >  |
        # ________________
        # |0,0_|0,1_|0,2_|
        # |1,0_|1,1_|1,2_|
        # 
        # [Grid Layour]

        buttonGrid = QGridLayout()

        for i, direction in enumerate(DIRECTION_DATAS):
            button = QPushButton(direction['label'])
            button.setObjectName(str(i))
            button.clicked.connect(self.onClickAction)

            pos = direction['position']
            buttonGrid.addWidget(button, pos[0], pos[1])

        layout = QVBoxLayout()
        layout.addWidget(self.mapView)
        layout.addLayout(buttonGrid)

        self.setLayout(layout)
        
        self.resize(500,500)

        self.__prepare()


    # def keyPressEvent(self, event: QKeyEvent):
    #     return super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event: QKeyEvent):

        tag = KEY_MAP.get(event.key(), -1)
        if tag < 0:
            return
        
        self.applyPlayerMove(str(tag))


    def onClickAction(self):
        sender = self.sender()
        tag = sender.objectName()

        self.applyPlayerMove(tag)

        
    def applyPlayerMove(self, tag):
        py,px = self.playerPos
        # TODO tag에 따라 플레이어를 이동
        # u,d,l,r

        direction = DIRECTION_DATAS[int(tag)]
        offset = direction['offset']
        dy,dx = py+offset[0],px+offset[1]

        dy = max(min(dy, self.maxRow), 0)
        dx = max(min(dx, self.maxCol), 0)

        # dy,dx 위치가 이동가능한 위치인지 파악
        if not self.checkMovable(dy, dx):
            return

        self.playerPos[:] = dy,dx
        self.displayMap()

    def __prepare(self):

        # 지도를 파일에서 불러오기
        self.loadMap()

        # 맵을 분석하여 시작위치와 도착위치 그리고 플레이어의 시작위치를 설정
        self.parsingMap()

        # 초기구성된 맵을 표시
        self.displayMap()


    def loadMap(self):

        with open('./res/level1.map', 'r') as f:
            while f.readable():
                line = f.readline()

                if not line:
                    break

                line = line.replace('\n', '').replace(' ', '')
                self.mapData.append(line)

            # print('self.mapData: ', self.mapData)
                
    def parsingMap(self):

        if len(self.mapData) <= 0:
            return

        self.maxRow = len(self.mapData)-1
        self.maxCol = len(self.mapData[0])-1

        # print(f'max: ({self.maxRow},{self.maxCol})')

        for y, line in enumerate(self.mapData):
            for x, tile in enumerate(line):
                if tile == 'S':
                    self.startPos = (y,x)

                if tile == 'F':
                    self.finishPos = (y,x)

        self.playerPos[:] = self.startPos[:]


    def displayMap(self):
        self.mapView.clear()

        py, px = self.playerPos
        for y, line in enumerate(self.mapData):

            # y,x 좌표가 플레이어의 위치와 같으면 'P'로 표시
            # str -> list
            li = list(line)
            if y == py:
                li[px] = 'P'

            # list -> str
            li = ''.join(li)
            self.mapView.append(li)

    def checkMovable(self, dy, dx) -> bool:
        
        # 제한영역내 좌표인지 확인
        # 이동가능한 위치(공간)인지 확인
        # inBound = (0 <= dy and dy <= self.maxRow) and (0 <= dx and dx <= self.maxCol)
        # if not inBound:
        #     return False
        # valid = self.mapData[dy][dx] != 'x'
        # return inBound and valid

        return self.mapData[dy][dx] != 'x'


if __name__ == '__main__':

    app = QApplication()

    window = MainWindow()
    window.show()

    app.exec_()







