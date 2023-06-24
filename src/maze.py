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


mapData = []
startPos = ()
finishPos = ()
playerPos = []
maxRow, maxCol = -1, -1

def prepare():
    # print('prepare')

    # 지도를 파일에서 불러오기
    loadMap()

    # 맵을 분석하여 시작위치와 도착위치 그리고 플레이어의 시작위치를 설정
    parsingMap()

    # 초기구성된 맵을 표시
    displayMap()



def loadMap():
    # print('loadMap')

    with open('./res/level1.map', 'r') as f:

        while f.readable():
            line = f.readline()
            # EOF => End of File

            if not line:
                break

            # line => 'o x o x x x x o F\n'
            # .split() => ['o','x','o'.....]
            # line = ''.join(line.split())
            # line = line.replace('\n', '')
            # line = line.replace(' ', '')
            line = line.replace('\n', '').replace(' ', '')
            mapData.append(line)

        # print(mapData)

def parsingMap():

    global startPos, finishPos, maxRow, maxCol

    maxRow = len(mapData)-1
    # 시작위치(S) 파악, 도착위치(F) 파악
    for y, line in enumerate(mapData):
        # print(line)
        maxCol = len(line)-1
        for x, tile in enumerate(line):
            
            if tile == 'S':
                startPos = (y,x)
                # print('startPos:', startPos)

            if tile == 'F':
                finishPos = (y,x)
                # print('finishPos:', finishPos)


        # .find() 찾는 값이 없을시 -1
        # .index() 찾는 값이 없을시 ValueError (예외발생)

        # x = line.find('S')
        # if x > -1:
        #     # 시작위치
        #     # (y,x)
        #     startPos = (y,x)
        #     print('startPos:', startPos)

        # x = line.find('F')
        # if x > -1:
        #     # 도착위치
        #     finishPos = (y,x)
        #     print('finishPos:', finishPos)

    # 플레이어의 위치를 초기지정
    playerPos[:] = startPos[:]
    print('playerPos:', playerPos)


def displayMap():

    # for y, line in enumerate(mapData):
    #     # print(line)
    #     for x, tile in enumerate(line):
    #         # # 플레이어의 위치(y,x)와 해당 타일의 위치(y,x)가 같다면 해당 타일의 표시는 'P'로 한다
    #         if playerPos[0] == y and playerPos[1] == x:
    #             # 해당 타일의 위치가 플레이어의 위치
    #             print('P', end='') #플레이어의 위치 'P'를 프린트
    #         else:
    #             print(tile, end='') #타일 값을 줄내림없이 프린트
    #     print() #줄내림만 프린트

    py, px = playerPos
    for y, line in enumerate(mapData):

        li = list(line)
        if y == py:
            # y축이 플레이어의 위치와 같다
            # x축의 인덱스와 동일한 위치에 값을 P로 변경하여 출력
            li[px] = 'P'
        
        print(''.join(li))

        # if y == py:
        #     # y축이 플레이어의 위치와 같다
        #     # x축의 인덱스와 동일한 위치에 값을 P로 변경하여 출력
        #     li = list(line)
        #     li[px] = 'P'
        #     print(''.join(li))
        # else:
        #     print(line)

# 게임플레이
def play():

    while True:
        os.system('clear')

        py, px = playerPos

        # TODO 현 플레이어의 위치가 도착위치라면 축하메세지를 띄우고 종료
        if finishPos[0] == py and finishPos[1] == px:
            print('축하합니다. 탈출에 성공하셨습니다.')
            
            break

        # 2.현 플레이어 위치에서 갈 수 있는 방향을 지문으로 표시 
        #   2-1.지문예시: 
        #      1) 북쪽으로 이동
        #      2) 동쪽으로 이동
        #      3) 남쪽으로 이동
        #      4) 서쪽으로 이동


        # 변경된 지도를 다시 표시
        displayMap()

        # 사용자가 이동할 방향에 대한 지문 표시
        print('Q. 진행하실 방향을 선택해주세요.')
        print('1.북')
        print('2.동')
        print('3.남')
        print('4.서')

        # 사용자의 입력을 받아옴 (사용자의 입력을 기다리며 코드 블럭)
        inputV = input('>>> ')

        # '3^2'
        # inputV.isdigit()   #숫자의 표현식도 포함
        # inputV.isdecimal() #int형으로 변환이 가능한것만!
        # inputV.isnumeric() #숫자의 표현식도 포함

        if inputV.isnumeric():

            # 3.플레이어가 선택한 지문의 방향으로 P를 이동시킴 (사용자의 입력을 기다리고 있음)
            #   조건1. 해당 방향의 한칸 이동한 위치가 in['o', 'F', 'S'] or != 'x'
            #   조건2. 지정된 범위안의 좌표인가? (dy >= 0 and dy <= 8) and (dx >= 0 and dx <= 8)
            #   3-1.선택한 방향이 유효하다면 플레이어의 현재위치를 이동위치로 변경
            #   3-2.선택한 방향이 비유효하다면 플레이어의 현재위치는 변동없음
            #     (진행이 불가하다는 메세지를 잠깐 표시하면 더좋음)

            # 1,2,3,4
            selection = int(inputV)

            if selection == 1:
                # 북
                dy, dx = py-1, px
                # TODO (dy,dx) 위치가 이동가능한 위치인지 확인!
                # 조건1. 지정된 범위안의 좌표인가? (dy >= 0 and dy <= 8) and (dx >= 0 and dx <= 8)
                # 조건2. 해당 방향의 한칸 이동한 위치가 in['o', 'F', 'S'] or != 'x'
                
                # error 버그, 글리치
                if checkMovable(dy, dx):
                    # 이동가능한 위치
                    # playerPos[0] = dy
                    # playerPos[1] = dx
                    # playerPos[0], playerPos[1] = dy, dx
                    playerPos[:] = (dy, dx)

            if selection == 2:
                # 동
                dy, dx = py, px+1
                if checkMovable(dy, dx):
                    playerPos[:] = (dy, dx)

            if selection == 3:
                # 남
                dy, dx = py+1, px
                if checkMovable(dy, dx):
                    playerPos[:] = (dy, dx)

            if selection == 4:
                # 서
                dy, dx = py, px-1
                if checkMovable(dy, dx):
                    playerPos[:] = (dy, dx)
        

        # 4.다시 2번부터 반복


def checkMovable(dy, dx) -> bool:

    inBoundary = (0 <= dy and dy <= maxRow) and (0 <= dx and dx <= maxCol) #조건1. 지정된 범위 확인
    validTile = (mapData[dy][dx] != 'x') #조건2. 지정된 타일 확인

    # if inBoundary and validTile:
    #     return True
    
    # return False

    return inBoundary and validTile











    

    pass



if __name__ == '__main__':
    prepare()

    play()


















class MainWindow(QWidget):
    def __init__(self, parent=None):

        # QLineEdit #한줄로만
        # QLabel #한줄로만
        # QTextEdit #다수의 줄을 지원

        self.mapView = QTextEdit(self)
        self.mapView.setText('')


    # def keyPressEvent(self, event: QKeyEvent) -> None:
    #     return super().keyPressEvent(event)
    
    # def keyReleaseEvent(self, event: QKeyEvent) -> None:
    #     return super().keyReleaseEvent(event)