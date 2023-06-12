#요구사항
# 유튜브에서 특정 영상을 다운받아 기록하는 것을 기반
# 1.유튜브영상을 스케치로 변경하여 저장
# 2.유튜브영상내에 특정컬러 추적하여 필터 후 저장
#   2-1.특정컬러의 영역에 사각테두리를 둘러서 표시
#   2-2.특정컬러의 영역만 마스킹하여 해당 컬러의 이미지만 색상이 있도록 (배경은 흑백)

#사용기술
# pafy or cap_from_youtube
# opencv
# hsv 컬러맵에 대한 이해 (yuv)

# # 빨간색 범위1
# lowerRed = np.array([0, 120, 70])
# upperRed = np.array([10, 255, 255])
# mask1 = cv2.inRange(hsv, lowerRed, upperRed)

# # 빨간색 범위2
# lowerRed = np.array([130, 120, 70])
# upperRed = np.array([180, 255, 255])
# mask2 = cv2.inRange(hsv, lowerRed, upperRed)

# mask = mask1 + mask2


import cv2
import numpy as np
from cap_from_youtube import cap_from_youtube


# 1. 스케치함수( cv2.pencilSketch() ) 사용에 대한 이해 (이전 코드를 참고)

# 이미지 -> 스케치로 -> 이미지
def toPencilSketch(origin:cv2.Mat) -> cv2.Mat:

    out = origin.copy()

    # 뿌옇도록 하는 효과
    out = cv2.GaussianBlur(out, ksize=(9, 9), sigmaX=0)
    '''
    sigma_s: Range between 0 to 200. Default 60.
    sigma_r: Range between 0 to 1. Default 0.07.
    shade_factor: Range between 0 to 0.1. Default 0.02.
    '''
    # 연필효과를 주는 함수
    out, color = cv2.pencilSketch(out, sigma_s=60, sigma_r=0.05, shade_factor=0.015)

    return out


def trackingColor(origin:cv2.Mat) -> cv2.Mat:

    frame = origin.copy()

    bgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 빨간색 범위1
    lowerRed = np.array([0, 120, 70])
    upperRed = np.array([10, 255, 255])
    mask1 = cv2.inRange(frameHSV, lowerRed, upperRed)
    # print('mask1.shape:', mask1.shape)

    # 빨간색 범위2
    lowerRed = np.array([130, 120, 70])
    upperRed = np.array([180, 255, 255])
    mask2 = cv2.inRange(frameHSV, lowerRed, upperRed)

    # cv2.add() => 화소의 값이 255를 넘으면 최대 255로 유지 255 + 1 = 255
    # + 연산자 => 화소의 값이 255를 넘으면 255 + 1 = 0
    # mask = mask1 + mask2
    mask = cv2.add(mask1, mask2)

    # ** bitwise_and() 의 src1 과 src2 의 색상 채널 수는 같아야한다
    redFrame = cv2.bitwise_and(frame, frame, mask=mask)
    # 컬러채널 수를 맞추고 and로 합성
    # maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    # redFrame = cv2.bitwise_and(frame, maskBGR)

    bgGray = cv2.cvtColor(bgGray, cv2.COLOR_GRAY2BGR)
    print('bgGray.shape:', bgGray.shape)

    out = cv2.bitwise_or(bgGray, redFrame)

    return out


url = "https://www.youtube.com/watch?v=QyBdhdz7XM4"

cap = cap_from_youtube(url, '480p')
if cap.isOpened():

    fps = cap.get(cv2.CAP_PROP_FPS)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 펜슬 스케치로 변경
        # out = frame.copy()
        # out = toPencilSketch(frame)

        # 특정색을 추적해서 배경은 흑백, 특정색만 컬러로 합성
        out = trackingColor(frame)
        
        cv2.imshow('video', out)
        if cv2.waitKey(int(1000/fps)) >= 0:
            break

        pass

cap.release()
cv2.destroyAllWindows()




