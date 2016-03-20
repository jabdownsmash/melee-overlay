
from PySide import QtCore, QtGui

class Container(QtGui.QWidget):
    def __init__(self, width,height,closeCallback, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMinimumSize(width,height)
        self.ccb = closeCallback

    def closeEvent(self, event):
        self.ccb()