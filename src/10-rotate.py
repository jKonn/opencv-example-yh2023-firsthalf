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

# 1. 라디안 각도 계산(60진법을 호도법으로 변경) 라디안 == 호도법
# 호 == rad 길이 60분법과 비율
# 60분법 == 360, 1도 = 60', 각도, 각분, 각초
# 1rad = pi / 180
d45 = 45.0 * np.pi/180 # 45도
d90 = 90.0 * np.pi/180 # 90도

# 2. 회전을 위한 변환 행렬 생성
# m45 = np.float32([[np.cos(d45), -1*np.sin(d45), rows//2],
#                   [np.sin(d45), np.cos(d45),    -1*cols//4]])

# 회전시 기준좌표를 기준으로 변환되기에 이미지의 위치가 변한다 (회전 반대반향으로 움직임)
# 변하는 위치만큼 보정해주어야 중앙에 위치할 수 있음
m45 = np.float32([[np.cos(d45), -1*np.sin(d45), rows*0.57],
                  [np.sin(d45), np.cos(d45),    -1*cols//4]])

m90 = np.float32([[np.cos(d90), -1*np.sin(d90), rows],
                  [np.sin(d90), np.cos(d90),    0]])

# 3. 회전 변환 행렬 적용
r45 = cv2.warpAffine(img, m45, (cols, rows))
r90 = cv2.warpAffine(img, m90, (rows, cols))

# 4. 결과
cv2.imshow('origin', img)
cv2.imshow('45', r45)
cv2.imshow('90', r90)

cv2.waitKey()
cv2.destroyAllWindows()