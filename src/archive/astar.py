import time
import os
from pprint import pprint
import math
import cmath
from copy import deepcopy
import heapq


# tile_map:tuple[tuple[str]] = [
#     ['o','x','o','x','x','x','x','o','F'],
#     ['o','o','o','x','x','o','o','o','x'],
#     ['o','x','o','x','o','o','x','o','x'],
#     ['o','o','o','o','o','x','x','o','o'],
#     ['x','x','x','x','o','o','x','x','x'],
#     ['o','o','o','o','x','o','o','o','o'],
#     ['x','o','x','o','o','o','x','o','x'],
#     ['o','o','o','o','x','o','o','o','x'],
#     ['S','x','x','o','o','x','x','o','x'],
# ]

tile_map:tuple[tuple[str]] = [
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

class CostOffset:
    cost = 0.0
    row = 0
    col = 0

    def __init__(self, offset:tuple[int], cost:float):
        self.row = offset[0]
        self.col = offset[1]
        self.cost = cost
        


# nodeDic = {
#     'parent':None,
#     'position':(None,None),
#     'func' : func1
# }

# nodeDic['func']

class TileNode:

    parent = None
    position:tuple[int] = None

    def __init__(self, position:tuple[int], parent = None):
        self.parent = parent
        self.position = position

        self.g = 0.0
        self.h = 0.0
        self.f = 0.0

    def __eq__(self, __o) -> bool:
        
        # if hasattr(__o, 'position'):
        #     return False

        if type(__o) != TileNode:
            return False

        # print(f'eq: {__o}')

        # return self.position == __o.position
        return self.position[0] == __o.position[0] and self.position[1] == __o.position[1]

    def __str__(self) -> str:
        return f'[TileNode] {self.position}, f={self.f:>.1f}, g={self.g:>.1f}, h={self.h:>.1f}'

    def __lt__(self, other):
        # print('__lt__')
        return self.f < other.f

        # if self.f < other.f:   #오름차순
        #     return True
        # # elif self.f == other.f:
        # #     return self.f > other.f  #첫번재 변수가 같으면 두번재 변수로 내림차순
        # else:
        #     return False

    # def equalPosition(self, node) -> bool:
    #     return self.position == node.position

    # def calculationCost():
    #     pass


debug_tile_map:tuple[tuple[str]] = deepcopy(tile_map)

MAX_COL:int = len(tile_map[0])
MAX_ROW:int = len(tile_map)

OFFSET_TOP = CostOffset((1,0), 1.0)
OFFSET_TOP_RIGHT = CostOffset((1,0), 2.0)
OFFSET_RIGHT = CostOffset((0,1), 1.0)
OFFSET_RIGHT_DOWN = CostOffset((-1,1), 2.0)
OFFSET_DOWN = CostOffset((-1,0), 1)
OFFSET_LEFT_DOWN = CostOffset((-1,-1), 2.0)
OFFSET_LEFT = CostOffset((0,-1), 1.0)
OFFSET_TOP_LEFT = CostOffset((1,-1), 2.0)
# 4방향
# OFFSETS:tuple[CostOffset] = (OFFSET_TOP, OFFSET_RIGHT, OFFSET_DOWN, OFFSET_LEFT) 
#8방향
OFFSETS:tuple[CostOffset] = (
    OFFSET_TOP, OFFSET_TOP_RIGHT, OFFSET_RIGHT, 
    OFFSET_RIGHT_DOWN, OFFSET_DOWN, OFFSET_LEFT_DOWN, 
    OFFSET_LEFT, OFFSET_TOP_LEFT
) 


start_tile:tuple[int] = (8,0)
finish_tile:tuple[int] = (0,8)

# DFS, BFS, 다익스트라

# 각 노드의 f,g,h 값을 파악해서 비용에 따른 길찾기
# g (현재 노드에서 출발 지점까지의 총 비용, 각노드의 이동방향에 따른 고정된 비용이 누적됨, 대각선이동이 가능할땐 피타고라스정의를 사용해서 대각선의 비용을 정의)
# h (Heuristic 휴리스틱, 현재 노드에서 목적지까지의 추정거리, 맨하튼거리 사용)
# f = g + h (총비용, 이 비용이 낮은것을 우선순위로 파악해 이동시 가장 낮은 비용을 들여 목적지에 도달 할 수 있는지를 파악)
def pathFinding(map_matrix:tuple[tuple[str]], start_pos:tuple[int], finish_pos:tuple[int]) -> list[tuple[int]]:

    open_list:list[TileNode] = []
    close_list:list[TileNode] = []
    # display_list:list[tuple] = []

    # 찾은 경로가 담김
    path:list[tuple[int]] = []

    # 처음에 시작위치의 노드를 넣고 시작
    # open_list.append(TileNode(start_pos))
    heapq.heappush(open_list, TileNode(start_pos))
    # print(open_list)

    # open_list가 비어있을때까지 반복
    while open_list:

        current_index = 0
        current_node = open_list[current_index]

        # heapq.heappop(open_list)

        # open_list 중에 가장 낮은 f값을 가진 노드를 가져옴
        # 주변노드를 파악해볼때 사용될 현재노드를 파악, f 값이 낮을수록 최단거리일 가능성이 높아서임
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_index = index
                current_node = node

        # open_list에서는 제외, close_list에 넣어둠
        # 이미 파악이 끝난 노드로 다시 확인되지 않도록 open_list에서 제외하고 close_list에 넣어둠
        # open_list.pop(current_index)
        del open_list[current_index]

        # print(f'node current_index: {current_index}')

        # current_node = heapq.heappop(open_list)
        close_list.append(current_node)

        # print(f'current_node: {current_node}')
        # displayMap(current_pos=current_node.position)


        # 현재 노드가 도착지인지 파악
        # 부모 노드를 역으로 따라서 추적하면 이동가능한 경로가 나옴 (트리구조)
        if current_node.position == finish_pos:
        # if current_node.position[0] == finish_pos[0] and current_node.position[1] == finish_pos[1]:

            # 현재 노드를 시작으로 부모노드를 추적해서 위치를 모아 경로를 구성
            path.append(current_node.position)
            parent_node: TileNode = current_node.parent
            
            # == 는 내부 __eq__ 를 사용하기에 is를 통해서 형을 비교
            while parent_node is not None:
                path.append(parent_node.position)

                # 해당 노드의 부모노드를 역으로 추적
                parent_node = parent_node.parent

            # 역으로 추적한거라 반대로 뒤집어주면 시작부터 순서대로 정렬됨
            path.reverse()
            return path


        # print('='*20)
        # print(f'current: {current_node}')

        # 현재노드 중심으로 이동가능한 방향의 오프셋을 모두 파악
        for offset in OFFSETS:

            child_row:int = current_node.position[0] + offset.row
            child_col:int = current_node.position[1] + offset.col
            
            # 유효한 범위내에 좌표인지 확인
            if child_col > MAX_COL - 1 or child_col < 0 or child_row > MAX_ROW - 1 or child_row < 0:
                continue

            # 이동이 가능한 위치인지 파악
            if map_matrix[child_row][child_col] == 'x':
                continue

            # close_list 에 포함되어있는 노드면 무시 및 다음 위치 확인 (이미 파악이 완료되었거나 파악중이거나)
            # 클래스내 __eq__ 메소드의 구현내용으로 비교 (== 연산자도 동일)
            child_node = TileNode((child_row, child_col), current_node)
            if child_node in close_list:
                # print('close_list에 포함된 노드')
                continue

            
            # f,g,h 값 업데이트
            # 시작위치에서 현재위치까지의 비용
            # child_node.g = current_node.g + (시작^2 - 도착^2)
            # TODO 여길 피타고라스 정의로 변경 하니 됨 (유클디안)
            child_node.g = current_node.g + math.hypot(current_node.position[0] - child_row, current_node.position[1] - child_col)
            # child_node.g = current_node.g + 10
            
            # 현재위치에서 목적지까지 장애물을 무시한 최단거리 비용
            # 맨하탄 거리 사용 ( 거리 = abs(현재.y - 목적지.y) + abs(현재.x - 목적지.x) )
            # 피타고라스 정의 사용 (유클디안)
            # child_node.h = abs(finish_pos[0] - child_row) + abs(finish_pos[1] - child_col)
            child_node.h = math.hypot(finish_pos[0] - child_row, finish_pos[1] - child_col)
            # 총비용 (g + h)
            child_node.f = child_node.g + child_node.h
            # print(f'[child_node] {child_node}')

            # print(f'[child_node] {child_node.position} g: {child_node.g:>.1f}, h: {child_node.h:>.1f}, f: {child_node.f:>.1f}')


            # open_list 에 포함되어 있고 g값이 더 큰 노드면 무시 및 다음 위치를 확인 
            # 동일한 탐색가능 위치지만 비용이 낮은 노드를 사용 (비교 위치에 따라서 누적되는 이동비용이 다름)
            # **단계가 진행되면서 시작위치와 멀어지기때문에 자식노드의 g보다 같거나 큰 중복노드를 찾아내면됨
            # **큰 g값만 무시하면 같은 g값의 노드가 중복으로 포함되어 계속 같은 자리를 돌게됨
            if [open_node for open_node in open_list if child_node == open_node and open_node.g <= child_node.g]:
                # print('open_list에 중복되었지만 g값이 더 큰 노드')
                continue

            # print(f'target: {target_node}')

            # 탐색이 가능한 open_list에 추가해두고 다음 탐색시 참조
            open_list.append(child_node)
            # heapq.heappush(open_list, child_node)

            # 맵의 내용 교체
            # debug_tile_map[child_node.position[0]][child_node.position[1]] = f'{child_node.h:.1f}'
            # debug_tile_map[child_node.position[0]][child_node.position[1]] = f'{child_node.f:.1f}'
            debug_tile_map[child_node.position[0]][child_node.position[1]] = f'@'


        debug_tile_map[start_pos[0]][start_pos[1]] = 'S'
        # debug_tile_map[current_node.position[0]][current_node.position[1]] = f'{child_node.h:.1f}'

        
        # for open_node in open_list:
        #     print(f'{open_node}')

        # print(f'{open_list}')
        # print(f'open_list length: {len(open_list)}')
        # print(f'close_list length: {len(close_list)}')

        os.system('clear')
        debugDisplayMap(current_pos=current_node.position)

        # display_list.append(current_node.position)
        # displayMap(path=display_list, current_pos=current_node.position)

        time.sleep(0.5)

    return path


def displayMap(path: tuple[tuple[str]] = (), current_pos: tuple[int] = None):

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

def debugDisplayMap(current_pos: tuple[int] = None):

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
displayMap(find_path)




