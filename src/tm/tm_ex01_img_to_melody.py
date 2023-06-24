import serial

import tensorflow as tf

# from tensorflow.keras.models import load_model
from keras.models import load_model
import cv2
import numpy as np

import threading, time


IMG_WIDTH = 224
IMG_HEIGHT = 224


lock = threading.Lock()

class Worker(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self) 
        self.daemon = True
 
    working = True
    def run(self):
        while self.working:
            if ser.readable():
                result = ser.readline()
                if not result:
                    time.sleep(0.1)
                    continue

                result = result.decode()
                result = result.replace('\r\n', '')
                # print(result, end='')
                # print(result)

                readMsg(result)               
                time.sleep(0.1)

        ser.close()

    # def stop(self):
    #     self.working = False
    #     # self.quit()
    #     # self.wait(5000)


playable = False

def prepare():
    np.set_printoptions(suppress=True)

    cv2.namedWindow("Img")
    cv2.setMouseCallback("Img", mouseEvent)

    global model, classNames, playable
    # model = load_model('./res/model/keras_model.h5')
    # classNames = open('./res/model/labels.txt', 'r').readlines()

    model = load_model('./res/tm_model_ma_li_te/keras_model.h5')
    classNames = open('./res/tm_model_ma_li_te/labels.txt', 'r').readlines()

    playable = False

def loop():

    global playable

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()
        if not ret:
            if cv2.waitKey(24) == 27:
                break

            continue

        # 티처블머신 스펙 (224 x 224) 이미지 크기로 설정
        image = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_AREA)
        cv2.imshow("Img", image)

        # print('playable:: ', playable)

        if playable:
            image = np.asarray(image, dtype=np.float32).reshape(1, IMG_WIDTH, IMG_HEIGHT, 3)
            image = (image / 127.5)-1 # 노멀라이즈, 0.0 ~ 1.0

            prediction = model.predict(image)
            index = np.argmax(prediction) # 가장 높은 값의 인덱스를 반환
            # print('prediction index: ', index)

            className = classNames[index]
            confidenceScore = prediction[0][index]

            # [prediction]
            # [
            #  [0.4, 1.0, 0.8]
            # ]

            # print('prediction: ', prediction)

            # print('confidenceScore: ', confidenceScore)
            print("Class:", className[2:], end="")
            # '1.1122'[:-2] => '1.11'
            print("Confidence Score:", str(np.round(confidenceScore * 100))[:-2], "%")

            if confidenceScore >= 0.5:
                # 아두이노로 시리얼통신을 통해 명령 전달
                sendMsg(str(index+1))
                playable = False

        if cv2.waitKey(24) == 27:
            break


def sendMsg(msg:str):
    ser.write(msg.encode()) #.encode() -> bytes 

def readMsg(msg:str):

    global playable

    # 쓰레드락
    lock.acquire()
    
    playable = msg == 'e'
    
    # 쓰레드 릴리즈
    lock.release()


def mouseEvent(event, x, y, flags, param):

    global playable

    if event == cv2.EVENT_LBUTTONDOWN:
        print('마우스 버튼 눌림')
        playable = True

    if event == cv2.EVENT_LBUTTONUP:
        print('마우스 버튼 떨어짐')
        playable = False
    

    # if event == cv2.EVENT_FLAG_LBUTTON:    
    #     cv2.circle(param, (x, y), radius, (255, 0, 0), 2)
    #     cv2.imshow("draw", src)

PORT = '/dev/ttyUSB0'

if __name__ == '__main__':

    ser = serial.serial_for_url(PORT, baudrate=9600, timeout=1)

    worker = Worker()
    worker.start()

    prepare()
    loop()
