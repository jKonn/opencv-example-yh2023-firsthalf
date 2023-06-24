import torch
import cv2
from cap_from_youtube import cap_from_youtube

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

model = torch.hub.load('ultralytics/yolov5', "yolov5s")
model.to(device) #현재 기본은 cuda
classNames = model.names

url = "https://www.youtube.com/watch?v=h3glVQbTmks"

# cap = cap_from_youtube(url, '480p')
cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS) # ex: 30fps, 60fps
mfps = int(1000/fps)  # ex: 16ms, 30ms
print('frameRate: ', fps)
print('mfps: ', mfps)

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # 프레임을 읽어와 표시(합성된 결과)

        # 해당 프레임을 yolo를 활용해 파악
        predict = model(frame)

        labels = predict.xyxyn[0][:,-1].cpu().numpy()
        cord = predict.xyxyn[0][:,:-1].cpu().numpy()

        # 결과를 프레임과 합성
        fy, fx = frame.shape[:2]

        labelNum = len(labels)
        for i in range(labelNum):
            # row => 해당 행의 값들이 담겨있음
            row = cord[i]
            x = row[4]
            if x >= 0.2:
                # 0.5 * 1080 = 540 = x1
                x1 = int(row[0]*fx)
                y1 = int(row[1]*fy)
                x2 = int(row[2]*fx)
                y2 = int(row[3]*fy)
                
                # labelStr = f'{classNames[int(labels[i])]}, ({x1},{y1}), {str(row[4])[:4]}'
                labelStr = '{}, ({},{}), {}'.format(
                                classNames[int(labels[i])],
                                x1,y1,
                                str(row[4])[:4]
                            )
                
                cv2.rectangle(frame, (x1,y1,x2,y2), (0,255,0), 2)
                cv2.putText(frame, labelStr, 
                            (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                            (0,0,255), 2)
                
        cv2.imshow('dst', frame)

    if cv2.waitKey(mfps) == 27:
        break

cap.release()
cv2.destroyAllWindows()
