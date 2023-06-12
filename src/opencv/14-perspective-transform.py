# mtrx = cv2.getPerspectiveTransform(pts1, pts2)
# pts1: 변환 이전 영상의 좌표 4개, 4 x 2 배열
# pts2: 변환 이후 영상의 좌표 4개, 4 x 2 배열
# mtrx: 변환행렬 반환, 3 x 3 행렬

import cv2
import numpy as np

path = './res/img1.jpeg'
img = cv2.imread(path)
rows, cols = img.shape[:2]

# 원근 변환 전 4개의 좌표
# topLeft(0,0), bottomLeft(0,h), topRight(w,0), bottomRights(w,h)
pts1 = np.float32([ [0,0], [0,rows], [cols,0], [cols,rows] ])
pts2 = np.float32([ [100,50], [10,rows-50], [cols-100, 50], [cols-10,rows-50] ])

# 변환 전 좌표를 표시
cv2.circle(img, (0,0), 10, (255,0,0), -1)
cv2.circle(img, (0,rows), 10, (255,0,0), -1)
cv2.circle(img, (cols,0), 10, (255,0,0), -1)
cv2.circle(img, (cols,rows), 10, (255,0,0), -1)

# 원근 변환 행렬 계산
mtrx = cv2.getPerspectiveTransform(pts1, pts2)

# 원근 변환 적용
dst = cv2.warpPerspective(img, mtrx, (cols, rows))

cv2.imshow('origin', img)
cv2.imshow('dst', dst)

cv2.waitKey()
cv2.destroyAllWindows()

