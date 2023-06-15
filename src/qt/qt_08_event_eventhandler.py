import PySide2.QtGui
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys



class MainWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # self.setMouseTracking(True)

        self.rightPress = False

        self.mousePosLocalLabel = QLabel('', self)
        # self.mousePosLocalLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.mousePosLocalLabel.resize(500,200)
        self.mousePosScreenLabel = QLabel('', self)
        # self.mousePosScreenLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.mousePosScreenLabel.resize(500,200)

        layout = QVBoxLayout(self)
        layout.addWidget(self.mousePosLocalLabel)
        layout.addWidget(self.mousePosScreenLabel)

        self.setLayout(layout)

        self.resize(500, 500)

        pass

    # def __str__(self):

    def mousePressEvent(self, event:QMouseEvent):
        # print('mousePressEvent event: ', event)

        # Qt.LeftButton 왼쪽버튼
        # Qt.RightButton 오른쪽버튼
        # event.button()

        if event.button() == Qt.RightButton:
            self.rightPress = True

        return
    
    def mouseReleaseEvent(self, event:QMouseEvent):
        # print('mouseReleaseEvent event: ', event)

        if event.button() == Qt.RightButton:
            self.rightPress = False

        return
    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        
        return
    
    def mouseMoveEvent(self, event:QMouseEvent):

        if self.rightPress:
            self.mousePosLocalLabel.setText(f'({event.x()}, {event.y()})')
            self.mousePosScreenLabel.setText(f'({event.globalX()}, {event.globalY()})')

        return
    


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()