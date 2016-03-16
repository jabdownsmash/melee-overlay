
from PySide import QtCore, QtGui

class Calibration(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        quit = QtGui.QPushButton("Calibrate")
        quit.resize(75, 30)
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        def buttonCB():
            self.calibrating = 2

        QtCore.QObject.connect(quit, QtCore.SIGNAL("clicked()"),buttonCB)
        quit.show()
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(quit, 0, 0)
        # gridLayout.addWidget(frameIndicator, 0, 1)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)
        # self.addWidget(frameIndicator)
        # self.show()
        self.rectangles = []
        self.texts = []
        self.kek = 0

        self.x1 = 0
        self.x2 = 100
        self.y1 = 0
        self.y2 = 0
        self.calibrating = 0

    def transformPoint(self,x,y):
        scale = (self.x2 - self.x1)/(88.47*2)
        xOffset = self.x1 + (self.x2 - self.x1)/2
        yOffset = (self.y1 + self.y2)/2

        return (x*scale + xOffset, y*scale + yOffset)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            print("xxx: ",x," y: ",y)
            # self.mcb(x,y)
            if self.calibrating == 2:
                self.x1 = x
                self.y1 = y
                self.calibrating -= 1
            elif self.calibrating == 1:
                self.x2 = x
                self.y2 = y
                self.calibrating -= 1
        self.update()