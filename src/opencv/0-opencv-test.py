import cv2

# imgPath

# 변수, 함수 소문자로 시작 ex variable, function
# 상수는 대문자 띄어쓰기는 _로 구분 CONST_VALUE
# 클래스는 대문자로 시작 ex Class

# imgPath = './res/img1.jpeg'
imgPath = '../res/img1.jpeg'

# 압축(encode)된 이미지 파일을 해석(decode)하여 Mat으로 구성 (=>행렬)
readImg = cv2.imread(imgPath)
print(readImg)

# None 타입이 아닐때! 이미지 화면에 표시
if readImg is not None:
    cv2.imshow('img', readImg)
    cv2.waitKey() #블럭 block
    cv2.destroyAllWindows()