
from PySide import QtCore, QtGui

class FrameIndicator(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.frame = 0
        self.numFrames = 7
        self.frameCounter = -1
        self.center = (self.numFrames - 1)/2
        self.alpha = 1

    def setFrame(self,frame):
        self.frame = frame
        self.update()

    def paintEvent(self,event):
        painter = QtGui.QPainter(self)

        for i in range(self.numFrames):
            if self.state == 'blank':
                painter.setPen(QtGui.QColor(55,55,55,self.alpha * 255))
                painter.setBrush(QtGui.QColor(55,55,55,self.alpha * 255))
            else: 
                if (i == 0 and self.frame <= -self.center and self.center > 0) or (i - self.center == self.frame and self.frame < 0):
                    painter.setPen(QtGui.QColor(55,55,255,self.alpha * 255))
                    painter.setBrush(QtGui.QColor(55,55,255,self.alpha * 255))
                elif ((i == self.numFrames - 1) and (self.frame >= self.numFrames - self.center) and self.center < (self.numFrames - 1)) or (i - self.center == self.frame and self.frame > 0):
                    painter.setPen(QtGui.QColor(255,55,55,self.alpha * 255))
                    painter.setBrush(QtGui.QColor(255,55,55,self.alpha * 255))
                elif self.frame == 0 and i == self.center:
                    painter.setPen(QtGui.QColor(255,255,255,self.alpha * 255))
                    painter.setBrush(QtGui.QColor(255,255,255,self.alpha * 255))
                else:
                    painter.setPen(QtGui.QColor(55,55,55,self.alpha * 255))
                    painter.setBrush(QtGui.QColor(55,55,55,self.alpha * 255))
            # painter.drawRect(QtCore.QRect(0, i * self.height()/self.numFrames, self.width(), self.height()/self.numFrames - self.height()/21))
            painter.drawRect(QtCore.QRect(i * self.width()/self.numFrames, 0, self.width()/self.numFrames - self.width()/21, self.height() - 1))
