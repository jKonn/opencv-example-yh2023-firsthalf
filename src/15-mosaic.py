import cv2
import numpy as np


# 모자이크 처리

rate = 15
winTitle = 'src'
img = cv2.imread('./res/img1.jpeg')

while True:
    # 마우스 드래그 이벤트가 발생 후 종료될때까지 블럭 (엔터 및 스페이스 등.. 입력 후)
    x,y,w,h = cv2.selectROI(winTitle, img, False)

    roi = img[y:y+h, x:x+w]
    # 리사이즈로 모자이크
    # roi = cv2.resize(roi, (w//rate, h//rate))
    # roi = cv2.resize(roi, (w,h), interpolation=cv2.INTER_AREA)

    # 평균으로 모자이크  
    
    # TODO: 모자이크 사이즈로 블럭을 나누어 화소평균을 적용해야 된다
    rh,rw = roi.shape[:2]
    bh,bw = rh//10, rw//10
    for y in range(0, 10):
        for x in range(0, 10):
            b = roi[y*bh:y*bh+bh, x*bw:x*bw+bw]
            roi[y*bh:y*bh+bh, x*bw:x*bw+bw] = cv2.mean(b)[:3]

    # roi = roi.astype(np.uint8)  
    # roi = cv2.mean(roi)[:3]

    # print('roi:', roi)

    # 블러로
    # roi = cv2.blur(roi, (10,10))

    img[y:y+h, x:x+w] = roi
    cv2.imshow(winTitle, img)

    # if w and h:
    #     roi = img[y:y+h, x:x+w]
    #     roi = cv2.resize(roi, (w//rate, h//rate))
    #     roi = cv2.resize(roi, (w,h), interpolation=cv2.INTER_AREA)
    #     img[y:y+h, x:x+w] = roi
    #     cv2.imshow(winTitle, img)
    # else:
    #     break

cv2.destroyAllWindows()