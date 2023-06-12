from PySide2.QtWidgets import *
# import PySide2.QtWidgets

import sys

if __name__ == '__main__':

    # app이라는 이름의 QApplication 클래스의 객체를 생성
    # QApplication 이 QT GUI 프로그램 그 자체
    app = QApplication(sys.argv)

    # window라는 이름의 QWidget 클래스(Class)의 객체(Object) 생성(인스턴스)
    window = QWidget()
    window.resize(289,170)
    window.setWindowTitle('첫번째 프로그램')

    # label라는 이름의 QLabel 클래스의 객체를 생성 (생성시 window 객체를 부모로 설정)
    label = QLabel('Hello Qt', window)
    label.move(110, 80) #위치정의 (position, (x,y) )

    # label = QLabel('Hello Qt')
    # label.setParent(window) #상위위젯(부모) 설정, 위젯이 소속된 공간
    # label.setText('Jkon')
    
    # 만들어서 설정해둔 객체를 화면에 표시
    window.show()

    # 해당 어플리케이션(QT어플리케이션)을 실행(동작, 런루프(RunLoops)))
    # 프로세스 - 쓰레드(메인)
    # 메인쓰레드
    app.exec_() #해당 위치에서 코드 블럭

    # print('hello')


# GUI <-> CUI(CLI)