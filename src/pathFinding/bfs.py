import time
import os
from copy import deepcopy

# tile_map = [
#     ['o','o','o','o','o','o','o','o','F'],
#     ['o','o','o','o','o','o','o','o','o'],
#     ['o','o','o','o','o','o','o','o','o'],
#     ['o','o','o','o','o','o','o','o','o'],
#     ['o','o','o','o','o','o','o','o','o'],
#     ['o','o','o','o','o','o','o','o','o'],
#     ['o','o','o','o','o','o','o','o','o'],
#     ['o','o','o','o','o','o','o','o','o'],
#     ['S','o','o','o','o','o','o','o','o'],
# ]

tile_map = [
    'ooooooooF',
    'ooooooooo',
    'ooooooooo',
    'ooooooooo',
    'ooooooooo',
    'ooooooooo',
    'ooooooooo',
    'ooooooooo',
    'Soooooooo',
]

class Node:
    def __init__(self, x, y, parent = None):
        self.parent = parent
        self.x = x
        self.y = y

    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y
    
    def __str__(self) -> str:
        return f'Node({self.x},{self.y})'


startPos = (8,0)
finishTile = (0,8)

finishNode = Node(8, 0)

OFFSET_U = (-1,0)
OFFSET_D = (1,0)
OFFSET_L = (0,-1)
OFFSET_R = (0,1)

OFFSET_UL = (-1,-1)
OFFSET_UR = (-1,1)
OFFSET_DL = (-1,-1)
OFFSET_DR = (-1,1)

# OFFSETS = [
#     OFFSET_U,
#     OFFSET_R,
#     OFFSET_D,
#     OFFSET_L,
# ]

OFFSETS = [
    OFFSET_U,
    OFFSET_UR,
    OFFSET_R,
    OFFSET_DR,
    OFFSET_D,
    OFFSET_DL,
    OFFSET_L,
    OFFSET_UL
]

def pathFinding():

    global path

    queue = []
    visited:list[Node] = []

    # 시작위치를 넣어준다
    queue.append(Node(0, 8))

    while queue:

        currentNode = queue.pop(0)
        # print('currentNode: ', currentNode)
        visited.append(currentNode)

        # S<-o<-o<-o<-o<-o<-o<-o<-F

        # 도착지점인지 확인
        # 도착지점이면 연결된 경로를 구성 종료
        if currentNode == finishNode:
            path = []

            pred = currentNode
            while pred is not None:
                path.append(pred)
                pred = pred.parent
            
            return

        for offset in OFFSETS:
            # print(offset)
            childX = currentNode.x + offset[1]
            childY = currentNode.y + offset[0]
            childNode = Node(childX, childY, currentNode)

            # 진행방향이 범위를 벗어났거나 장애물일 경우 무시
            if (0 > childX or childX > 8) or (0 > childY or childY > 8):
                continue

            if [vi for vi in visited if childNode == vi]:
                continue

            if [q for q in queue if childNode == q]:
                continue
            
            queue.append(childNode)


    # 방문한 순서대로 지도에 표시
    for vi in visited:
        # os.system('clear')
        os.system('cls')
        # print(vi)

        # 해당 노드를 지도에 표시
        displayMap(vi.x, vi.y)
        time.sleep(0.5)



def displayMap(nodeX,nodeY):

    map = deepcopy(tile_map)

    # 대입
    # li = [1,2,3]
    # li2 = li

    # 얕은복사
    # li3 = []
    # li3[:] = li[:]
    # li4 = li[:]

    # 깊은복사
    # li5 = deepcopy(li)

    for y, line in enumerate(map):

        if y == nodeY:
            li = list(line)
            li[nodeX] = '@'
            map[y] = ''.join(li)

        print(map[y])


def displayPath():
    # for p in path:
    #     print(p)

    map = deepcopy(tile_map)

    # 경로에 해당하는 타일의 값을 변경
    for node in path:
        line = map[node.y]
        li = list(line)
        li[node.x] = '*'
        map[node.y] = ''.join(li)
    
    for y, line in enumerate(map):
        print(line)


if __name__ == '__main__':
    pathFinding()

    # 시작부터 도착지점까지의 경로 출력
    displayPath()