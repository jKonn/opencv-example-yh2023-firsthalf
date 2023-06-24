import time
import os
from pprint import pprint
import math
import cmath
from copy import deepcopy
import heapq

tile_map = [
    ['o','o','o','o','o','o','o','o','F'],
    ['o','o','o','o','o','o','o','o','o'],
    ['o','o','o','o','o','o','o','o','o'],
    ['o','o','o','o','o','o','o','o','o'],
    ['o','o','o','o','o','o','o','o','o'],
    ['o','o','o','o','o','o','o','o','o'],
    ['o','o','o','o','o','o','o','o','o'],
    ['o','o','o','o','o','o','o','o','o'],
    ['S','o','o','o','o','o','o','o','o'],
]


class TileNode:

    def __init__(self, position, predecessor = None):
        self.position = position
        self.predecessor = predecessor
        self.f = 0

    def __eq__(self, __o) -> bool:
        
        # if hasattr(__o, 'position'):
        #     return False
        if type(__o) != TileNode:
            return False

        # print(f'eq: {__o}')

        # return self.position == __o.position
        return self.position[0] == __o.position[0] and self.position[1] == __o.position[1]

    def __str__(self) -> str:
        return f'[TileNode] {self.position}'

    def __lt__(self, other):
        # print('__lt__')
        return self.f < other.f


debug_tile_map = deepcopy(tile_map)

MAX_COL:int = len(tile_map[0])
MAX_ROW:int = len(tile_map)


OFFSET_TOP = (1,0)
OFFSET_TOP_RIGHT = (1,0)
OFFSET_RIGHT = (0,1)
OFFSET_RIGHT_DOWN = (-1,1)
OFFSET_DOWN = (-1,0)
OFFSET_LEFT_DOWN = (-1,-1)
OFFSET_LEFT = (0,-1)
OFFSET_TOP_LEFT = (1,-1)


# 4방향
#   0
# 0 1 0
#   0
# OFFSETS:tuple[int] = (OFFSET_TOP, OFFSET_RIGHT, OFFSET_DOWN, OFFSET_LEFT) 

#8방향
# 0 0 0
# 0 1 0
# 0 0 0
OFFSETS = (
    OFFSET_TOP, OFFSET_TOP_RIGHT, OFFSET_RIGHT,  # type: ignore
    OFFSET_RIGHT_DOWN, OFFSET_DOWN, OFFSET_LEFT_DOWN, 
    OFFSET_LEFT, OFFSET_TOP_LEFT
)


start_tile = (8,0)
finish_tile = (0,8)


def pathFinding(map_matrix, start_pos, finish_pos):

    node_queue:list[TileNode] = []
    visited_list:list[TileNode] = []

    # 찾은 경로가 담김
    path:list[tuple[int]] = []

    # 처음에 시작위치의 노드를 넣고 시작
    node = TileNode(start_pos)
    node_queue.append(node)
    # print(node_queue)

    # node_queue 가 비어있을때까지 반복
    while node_queue:

        # 가장 오래전에 넣어둔 노드를 꺼냄
        current_node = node_queue.pop(0)
        # print(f'current_node: {current_node}')

        # 방문목록에 추가
        visited_list.append(current_node)
        
        # 현재 노드가 도착지인지 파악
        if current_node.position[0] == finish_pos[0] and current_node.position[1] == finish_pos[1]:

            predecessor:TileNode = current_node

            # predecessor 를 추적해서 경로 구성
            while predecessor is not None:
                path.append(predecessor.position)
                predecessor = predecessor.predecessor # type: ignore

            # # 방문한 목록을 경로로 구성
            # for visited_node in visited_list:
            #     path.append(visited_node.position)

            return path


        # print('='*20)
        # print(f'current: {current_node}')

        # 현재노드 중심으로 이동가능한 방향의 오프셋을 모두 파악
        for offset in OFFSETS:

            child_row = current_node.position[0] + offset[0]
            child_col = current_node.position[1] + offset[1] # type: ignore
            
            # 유효한 범위내에 좌표인지 확인
            if child_col < 0 or child_col > MAX_COL - 1 or child_row < 0 or child_row > MAX_ROW - 1:
                continue

            # 이동이 가능한 위치인지 파악
            if map_matrix[child_row][child_col] == 'x':
                continue

            child_node = TileNode((child_row, child_col), current_node) #현재노드의 자식노드를 생성

            # 이미 방문한 노드와 큐에 추가된 노드는 중복 확인하지 않음
            #방문목록(visited_list)에 포함되었거나, 예정목록(node_queue)에 포함이면 무시
            if (child_node in visited_list) or (child_node in node_queue): # 클래스내 __eq__ 메소드의 구현내용으로 비교 (== 연산자도 동일)
                continue

            # 탐색이 가능한 노드를 node_queue 추가해두고 다음 탐색시 참조
            node_queue.append(child_node)

            # 맵의 내용 교체
            # debug_tile_map[child_node.position[0]][child_node.position[1]] = f'{child_node.position}'
            debug_tile_map[child_node.position[0]][child_node.position[1]] = f'@'

        
        # print(f'node_queue length: {len(node_queue)}')

        # debug_tile_map[start_pos[0]][start_pos[1]] = 'S'

        os.system('cls')
        debugDisplayMap(current_pos=current_node.position)

        time.sleep(0.5)

    return path


def displayMap(path, current_pos = None):

    # 더이상 나열이 불가한 최소 단위의 항목을 하나씩 가져옴
    for row, datas in enumerate(tile_map):
        # 한번 반복에 최대 9개까지 출력
        for col, data in enumerate(datas):
            # 최대 9번 반복
            # print(f'{row,col}', end=',')
            # print(data, end=' ')

            # 해당 위치가 경로에 포함이라면 표시
            pos = (row, col)

            # if current_pos and current_pos == pos:
            if current_pos and current_pos[0] == pos[0] and current_pos[1] == pos[1]:
                print('@', end=' ')
            elif pos == start_tile or pos == finish_tile:
                print(data, end=' ')
            elif pos in path:
                print('◼︎', end=' ')
            else:
                print(data, end=' ')
                
        print()

def debugDisplayMap(current_pos):

    # 더이상 나열이 불가한 최소 단위의 항목을 하나씩 가져옴
    for row, datas in enumerate(debug_tile_map):
        # 한번 반복에 최대 9개까지 출력
        for col, data in enumerate(datas):
            pos = (row, col)
            if current_pos and current_pos[0] == pos[0] and current_pos[1] == pos[1]:
                print(f'{"@":<4}', end=' ')
            else:
                print(f'{data:<4}', end=' ')
        print(end='\n\n')

# display_map()
# print()

find_path = pathFinding(map_matrix=tile_map, start_pos= start_tile, finish_pos = finish_tile)
# print(find_path)

# for idx, path in enumerate(find_path):
#     print(f'[{idx+1}]{path}')
displayMap(find_path)




