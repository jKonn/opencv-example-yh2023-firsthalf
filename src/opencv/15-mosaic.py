import cv2
import numpy as np


def mosaicWithAvg(src:cv2.Mat, blockSize:int) -> cv2.Mat:
    

    dst = src.copy()
    
    rh,rw = dst.shape[:2]
    bh,bw = rh // blockSize, rw // blockSize
    for y in range(0, blockSize):
        for x in range(0, blockSize):
            b = dst[y*bh:y*bh+bh, x*bw:x*bw+bw]
            dst[y*bh:y*bh+bh, x*bw:x*bw+bw] = cv2.mean(b)[:3]

    return dst


# 모자이크 처리

rate = 15
winTitle = 'src'
img = cv2.imread('./res/img1.jpeg')

while True:
    # 마우스 드래그 이벤트가 발생 후 종료될때까지 블럭 (엔터 및 스페이스 등.. 입력 후)
    x,y,w,h = cv2.selectROI(winTitle, img, False)
    if w and h:
        roi = img[y:y+h, x:x+w]
        # 리사이즈로 모자이크
        # roi = cv2.resize(roi, (w//rate, h//rate))
        # roi = cv2.resize(roi, (w,h), interpolation=cv2.INTER_AREA)

        # 평균으로 모자이크  
        # 모자이크 사이즈로 블럭을 나누어 화소평균을 적용
        roi = mosaicWithAvg(roi, 10)
        # print('roi:', roi)

        # 블러로
        # roi = cv2.blur(roi, (10,10))

        img[y:y+h, x:x+w] = roi
        cv2.imshow(winTitle, img)
    else:
        break

cv2.destroyAllWindows()