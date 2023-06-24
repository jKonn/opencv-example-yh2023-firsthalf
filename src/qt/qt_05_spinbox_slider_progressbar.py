import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = QWidget()

    spin = QSpinBox()
    spin.setRange(0,100)

    slider = QSlider(Qt.Horizontal)
    slider.setRange(0,100)

    progressBar = QProgressBar()
    progressBar.setAlignment(Qt.AlignCenter)
    progressBar.setRange(0,100)

    spin.valueChanged.connect(slider.setValue)
    spin.valueChanged.connect(progressBar.setValue)
    slider.valueChanged.connect(spin.setValue)

    layout = QHBoxLayout()
    layout.addWidget(spin)
    layout.addWidget(slider)
    layout.addWidget(progressBar)

    form.setLayout(layout)
    form.setWindowTitle('SpinSliderProgressDemo')
    
    form.show()

    screens = QApplication.screens()
    print('screens: ', screens)

    screenSize = screens[1].availableSize()

    # screenSize = QApplication.primaryScreen().availableSize()
    print('screenSize: ', screenSize)

    formSize = form.sizeHint()
    print('formSize: ', formSize)


    form.move(
        (screenSize.width()//2) - (formSize.width()//2), #x
        (screenSize.height()//2) - (formSize.height()//2) #y
    )

    app.exec_()