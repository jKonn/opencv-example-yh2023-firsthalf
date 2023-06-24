import time
import os

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

display_map = []


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

OFFSET_U = (-1,0)
OFFSET_D = (1,0)
OFFSET_L = (0,-1)
OFFSET_R = (0,1)

OFFSETS = [
    OFFSET_U,
    OFFSET_R,
    OFFSET_D,
    OFFSET_L,
]

def pathFinding():

    queue = []
    visited:list[Node] = []

    queue.append(Node(0, 8))

    while queue:

        currentNode = queue.pop(0)
        # print('currentNode: ', currentNode)
        visited.append(currentNode)

        for offset in OFFSETS:
            # print(offset)
            childX = currentNode.x + offset[1]
            childY = currentNode.y + offset[0]
            childNode = Node(childX, childY, currentNode)


            # 진행방향이 범위를 벗어났거나 장애물일 경우 무시
            if (0 > childX or childX > 8) or (0 > childY or childY > 8):
                # print(childX)
                # print(childY)
                continue

            if [vi for vi in visited if childNode == vi]:
                continue

            # exists = False
            # for vi in visited:
            #     # if childX == vi.x and childY == vi.y:
            #     if childNode == vi:
            #         exists = True
            #         continue

            # if exists:
            #     continue
            
            queue.append(childNode)
            break

    for vi in visited:
        # os.system('clear')
        os.system('cls')
        # print(vi)

        # 해당 노드를 지도에 표시
        displayMap(vi.x, vi.y)
        time.sleep(0.5)

def displayMap(nodeX,nodeY):
    for y, line in enumerate(tile_map):

        if y == nodeY:
            li = list(line)
            li[nodeX] = '@'
            tile_map[y] = ''.join(li)

        print(tile_map[y])


if __name__ == '__main__':
    pathFinding()