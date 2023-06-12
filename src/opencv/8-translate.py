import cv2
import numpy as np

img = cv2.imread('./res/img1.jpeg')
rows,cols = img.shape[0:2] # 영상의 크기

# dst = cv2.warpAffine(src, matrix, dsize, dst, flags, borderMode, borderValue)
# src: 원본 이미지, numpy 배열
# matrix: 2 x 3 변환행렬, dtype=float32
# dsize: 결과 이미지의 크기, (width, height)
# flags(optional): 보간법 알고리즘 플래그
# borderMode(optional): 외곽 영역 보정 플래그
# borderValue(optional): cv2.BORDER_CONSTANT 외곽 영역 보정 플래그일 경우 사용할 색상 값 (default=0)
# dst: 결과 이미지

# 이동할 픽셀 거리
dx, dy = 100, 50
# dx, dy = 500, 500

# 1. 변환 행렬 생성
mtrx = np.float32([ [1,0,dx],
                    [0,1,dy] ])

# 2. 단순 이동
dst = cv2.warpAffine(img, mtrx, (cols+dx, rows+dy))


# 3. 탈락된 외곽 픽셀을 파랑색으로 보정
dst2 = cv2.warpAffine(img, mtrx, (cols+dx, rows+dy), None, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, (255,0,0))
# dst2 = cv2.warpAffine(img, mtrx, (cols+dx, rows+dy), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,0,0))

# 4. 탈락된 외곽 픽셀을 원본을 반사 시켜서 보정
dst3 = cv2.warpAffine(img, mtrx, (cols+dx, rows+dy), None, cv2.INTER_LINEAR, cv2.BORDER_REFLECT)

cv2.imshow('original', img)
# cv2.imshow('trans', dst)
cv2.imshow('trans', dst2)
# cv2.imshow('trans', dst3)

cv2.waitKey(0)
cv2.destroyAllWindows()