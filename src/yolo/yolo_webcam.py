import torch
import cv2
import time

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

# cuda = torch.device(device)

# Model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")
# model.cuda()
# model.to(device)
# model.to('cuda')
# model.to('cpu')

classes = model.names

cap = cv2.VideoCapture(0)

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        if cv2.waitKey(1) == 27:
            break
        continue

    now = time.time()
    
    # TODO 모델을 활용해서 객체를 탐색하고 탐색된 결과를 합성
    
    # 모델을 통해 해당 프레임을 분석
    predict = model(frame) #해당 프레임의 이미지를 특정 모델을 통해 이미지속 사물을 파악

    labels = predict.xyxyn[0][:,-1].cpu().numpy()  #파악된 결과속 정보 중 라벨만 읽어옴 (narray로 구성)
    cord = predict.xyxyn[0][:,:-1].cpu().numpy()   #파악된 결과속 정보 중 위치만 읽어옴 (narray로 구성)

    # 읽어온 정보를 기반으로 합성
    frameY, frameX = frame.shape[:2]

    for i in range(len(labels)):
        row = cord[i]
        if row[4] >= 0.2:
            x1 = int(row[0]*frameX)
            y1 = int(row[1]*frameY)
            x2 = int(row[2]*frameX)
            y2 = int(row[3]*frameY)

            labelStr = f'{classes[int(labels[i])]}, ({x1},{x2}), {str(row[4])[:4]}'

            cv2.rectangle(frame, (x1,y1,x2,y2), (0,255,0), 2)
            cv2.putText(frame, labelStr, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow('origin', frame)

    if cv2.waitKey(1) == 27:
        break

    delta = time.time() - now
    print(delta)