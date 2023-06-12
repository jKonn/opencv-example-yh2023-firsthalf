import cv2
import pafy

url = "https://www.youtube.com/watch?v=QyBdhdz7XM4"

# 해당 url의 영상 다운로드
videoInfo = pafy.new(url)
print('videoInfo: ', videoInfo)

best = videoInfo.getbest(preftype='mp4')

# 캡쳐 구성
videoPath = best.url

cap = cv2.VideoCapture(videoPath)

fps = cap.get(cv2.CAP_PROP_FPS)
print('frameRate: ', fps)

if cap.isOpened():

    # 영상 기록이 가능한 구조
    # 녹화정의
    saveFilePath = './record.avi'
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    # cap 내에 있는 영상에 대한 정의 중 크기를 가져옴
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = int(width), int(height)

    # VideoWriter 객체 생성 (어떻게 파일을 저장할건지에 대한 정의)
    out = cv2.VideoWriter(saveFilePath, fourcc, fps, size)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 캡쳐된 프레임을 표시
        cv2.imshow('video', frame)

        # 캡쳐된 프레임을 기록 (저장)
        out.write(frame)
        # cv2.imwrite()

        if cv2.waitKey(int(1000/fps)) >= 0:
            break

    # **저장하는 버퍼를 닫아줌
    out.release()
    pass

cap.release()
cv2.destroyAllWindows()




