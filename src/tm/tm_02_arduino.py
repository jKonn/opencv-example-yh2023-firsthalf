import serial

import tensorflow as tf
from keras.models import load_model
import cv2
import numpy as np


IMG_WIDTH = 224
IMG_HEIGHT = 244


def prepare():

    global model, classNames

    np.set_printoptions(suppress=True)

    model = load_model('./res/model/keras_model.h5')
    classNames = open('./res/model/labels.txt', 'r').readlines()

def loop():

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()
        if not ret:
            if cv2.waitKey(24) == 27:
                break

            continue

        # 티처블머신 스펙 (224 x 224) 이미지 크기로 설정
        image = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_AREA)
        cv2.imshow("Webcam Image", image)

        image = np.asarray(image, dtype=np.float32).reshape(1, IMG_WIDTH, IMG_HEIGHT, 3)
        image = (image / 127.5)-1 # 노멀라이즈, 0.0 ~ 1.0

        prediction = model.predict(image)
        index = np.argmax(prediction) # 가장 높은 값의 인덱스를 반환
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

        if cv2.waitKey(24) == 27:
            break


def sendMsg(msg):
    ser.write(msg.encode()) #.encode() -> bytes 


PORT = '/dev/ttyUSB0'
if __name__ == '__main__':

    ser = serial.serial_for_url(PORT, baudrate=9600, timeout=1)

    prepare()
    loop()
