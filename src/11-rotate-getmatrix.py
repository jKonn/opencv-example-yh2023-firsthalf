import cv2
import numpy as np


# dst = cv2.warpAffine(src, matrix, dsize, dst, flags, borderMode, borderValue)
# src: 원본 이미지, numpy 배열
# matrix: 2 x 3 변환행렬, dtype=float32
# dsize: 결과 이미지의 크기, (width, height)
# flags(optional): 보간법 알고리즘 플래그
# borderMode(optional): 외곽 영역 보정 플래그
# borderValue(optional): cv2.BORDER_CONSTANT 외곽 영역 보정 플래그일 경우 사용할 색상 값 (default=0)
# dst: 결과 이미지

img = cv2.imread('./res/img1.jpeg')
rows,cols = img.shape[:2]

center = (cols/2, rows/2)

# 1. 회전을 위한 변환 행렬 구하기
# 회전축:중앙, 각도:45, 배율:0.5

# mtrx = cv2.getRotationMatrix2D(center, angle, scale)
# center: 회전축 중심 좌표 (x, y)
# angle: 회전할 각도, 60진법
# scale: 확대 및 축소비율

m45 = cv2.getRotationMatrix2D(center, -45, 0.5)
img45 = cv2.warpAffine(img, m45, (cols, rows))

# 2. 회전을 위한 변환 행렬 구하기
# 회전축:중앙, 각도:90, 배율:1.5

m90 = cv2.getRotationMatrix2D(center, 90, 1.5)
img90 = cv2.warpAffine(img, m90, (cols, rows))

# cv2.imshow('45', img45)
cv2.imshow('90', img90)

cv2.waitKey()
cv2.destroyAllWindows()