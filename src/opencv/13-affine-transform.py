import cv2
import numpy as np

# martix = cv2.getAffineTransform(pts1, pts2)
# pts1: 변환 전 영상의 좌표 3개, 3 x 2 배열
# pts2: 변환 후 영상의 좌표 3개, 3 x 2 배열
# matrix: 변환 행렬 반환, 2 x 3 행렬


path = './res/img1.jpeg'
img = cv2.imread(path)
rows, cols = img.shape[:2]

# 변환 전,후 각 3개의 좌표 생성
pts1 = np.float32([[200,150], [300,150], [200,300]])
pts2 = np.float32([[180,170], [310,160], [350,220]])

# 변환 전 좌표를 이미지에 표시
cv2.circle(img, (200,150), 5, (250,0,0), -1)
cv2.circle(img, (300,150), 5, (0,255,0), -1)
cv2.circle(img, (200,300), 5, (0,0,255), -1)

# 변환 행렬 생성
mtrx = cv2.getAffineTransform(pts1, pts2)

# 어핀 변환 적용
dst = cv2.warpAffine(img, mtrx, (int(cols*1.5), rows))

# 결과출력
cv2.imshow('origin', img)
cv2.imshow('dst', dst)
cv2.waitKey()
cv2.destroyAllWindows()