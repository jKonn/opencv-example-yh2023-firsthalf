import cv2
import numpy as np
# import hello

# 절차적(c), 객체지향형(c++) -> (완전 객체지향형)(java), 함수형
# c언어 함수를 기반으로 만든언어 

winTitle = 'dst'

# onMouse(event,x,y,flags,param)
# event: 마우스 이벤트 종류
# x,y: 마우스 이벤트가 발생한 좌표
# flags: 마우스 이벤트 발생시 상태
# param: cv2.setMouseCallback() 함수에서 설정한 데이터 (임의데이터)

# 리퀴파이 
def liquify(img, cx1,cy1, cx2,cy2):

    # 대상 영역 좌표와 크리 설정
    x,y,w,h = cx1-half, cy1-half, half*2, half*2 

    # 관심영역 설정
    roi = img[y:y+h, x:x+w].copy()
    out = roi.copy()

    # 관심역역 기준으로 좌표 재 설정 (오프셋 == 변위 == 거리)
    offset_cx1, offset_cy1 = cx1-x, cy1-y
    offset_cx2, offset_cy2 = cx2-x, cy2-y

    # 변환 이전 4개의 삼각형 좌표
    tri1 = [
        [ (0,0), (w,0), (offset_cx1,offset_cy1) ],  #top
        [ (0,0), (0,h), (offset_cx1,offset_cy1) ],  #left
        [ (w,0), (offset_cx1,offset_cy1), (w,h) ],  #right
        [ (0,h), (offset_cx1,offset_cy1), (w,h) ],  #bottom
    ]

    # 변환 이후 4개의 삼각형 좌표
    tri2 = [
        [ (0,0), (w,0), (offset_cx2,offset_cy2) ],  #top
        [ (0,0), (0,h), (offset_cx2,offset_cy2) ],  #left
        [ (w,0), (offset_cx2,offset_cy2), (w,h) ],  #right
        [ (0,h), (offset_cx2,offset_cy2), (w,h) ],  #bottom
    ]

    for i in range(4):
        # 어핀변환 적용 (변환행렬 생성 및 적용)
        matrix = cv2.getAffineTransform(np.float32(tri1[i]), np.float32(tri2[i]))
        warped = cv2.warpAffine(roi.copy(), matrix, (w,h), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

        # 삼각형 모양의 마스크 생성
        mask = np.zeros((h,w), dtype=np.uint8)
        mask = cv2.fillConvexPoly(mask, np.int32(tri2[i]), (255,255,255))
        # cv2.imshow('mask', mask)

        # 마스킹 후 합성
        # 변형된 대상과 배경을 나눠서 클립하고, 둘을 합쳐서 결과를 낸다
        warped = cv2.bitwise_and(warped, warped, mask=mask)
        # warped = cv2.copyTo(warped, mask=mask)
        out = cv2.bitwise_and(out, out, mask=cv2.bitwise_not(mask))
        out = out + warped
    
    img[y:y+h, x:x+w] = out
    return img


isDragging = False
half = 50

def onMouse(event, x,y, flags, param):

    global cx1, cy1, isDragging, img

    if event == cv2.EVENT_MOUSEMOVE:

        # 드래그영역 표시
        if not isDragging:
            imgDraw = img.copy()
            # 드래그 영역 표시
            cv2.rectangle(imgDraw, (x-half, y-half), (x+half, y+half), (0,255,0))
            cv2.imshow(winTitle, imgDraw)

        # if isDragging:
        #     print(f'mouse 좌표: ({x},{y})')

        pass
    elif event == cv2.EVENT_LBUTTONDOWN:
        # 드래그 상태
        print(f'mouse 드래그 시작!')

        isDragging = True
        cx1, cy1 = x, y

        pass
    elif event == cv2.EVENT_LBUTTONUP:
        # 드래그 끝
        # 리퀴파이 적용 

        print(f'mouse 드래그 끝!')

        if isDragging:
            isDragging = False

            img = liquify(img, cx1, cy1, x, y)
            cv2.imshow(winTitle, img)

        pass

    pass

if __name__ == '__main__':
    
    img = cv2.imread('./res/img1.jpeg')
    h,w = img.shape[:2]

    cv2.namedWindow(winTitle)
    cv2.setMouseCallback(winTitle, onMouse)
    cv2.imshow(winTitle, img)

    while True:
        key = cv2.waitKey(1)
        if key & 0xFF == 27:
            break
    
    cv2.destroyAllWindows()