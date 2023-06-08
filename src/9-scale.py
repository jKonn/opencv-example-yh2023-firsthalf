import cv2
import numpy as np

img = cv2.imread('./res/img1.jpeg')
height, width = img.shape[:2]

# array, list
# 다수의 자료를 포함, 순서가 있고 시작이 0번, 인덱스가 숫자형식의 번호로 구성
#        0,1,2,3,4,5,6,7......
# list = [1,2,3,4,5,6,7,7], 원소의 자료형이 모두 같아야한다???
# list[0], list[1], list[5]

# [][0] => [1,1,1,1,1,1,1,1][0] => 1 == [0][0] => (row,col) => (0,0)
# 행렬
# [
#   [1,1,1,1,1,1,1,1],
#   [2,2,2,2,2,2,2,2],
#   [3,3,3,3,3,3,3,3],
#   [4,4,4,4,4,4,4,4],
#   [5,5,5,5,5,5,5,5],
# ]
# 1920 * 1080 * 3 * 60

# dst = cv2.warpAffine(src, matrix, dsize, dst, flags, borderMode, borderValue)
# src: 원본 이미지, numpy 배열
# matrix: 2 x 3 변환행렬, dtype=float32
# dsize: 결과 이미지의 크기, (width, height)
# flags(optional): 보간법 알고리즘 플래그
# borderMode(optional): 외곽 영역 보정 플래그
# borderValue(optional): cv2.BORDER_CONSTANT 외곽 영역 보정 플래그일 경우 사용할 색상 값 (default=0)
# dst: 결과 이미지


smallFactor = 0.2
bigFactor = 3

# 1. 0.5배 축소 변환 행렬
m_small = np.float32([ [smallFactor,           0, 0],
                       [          0, smallFactor, 0] ])

m_big = np.float32([ [bigFactor,         0, 0],
                     [0,         bigFactor, 0] ])

small_dsize = (int(width*smallFactor),int(height*smallFactor))
dst1 = cv2.warpAffine(img, m_small, small_dsize)

big_dsize = (int(width*bigFactor),int(height*bigFactor))
dst2 = cv2.warpAffine(img, m_big, big_dsize)

dst3 = cv2.warpAffine(img, m_small, small_dsize, None, cv2.INTER_AREA)
dst4 = cv2.warpAffine(img, m_big, big_dsize, None, cv2.INTER_CUBIC)


cv2.imshow('original', img)
# cv2.imshow('small', dst1)
# cv2.imshow('big', dst2)
cv2.imshow('small_INTER_AREA', dst3)
cv2.imshow('big_INTER_CUBIC', dst4)


cv2.waitKey()
cv2.destroyAllWindows()