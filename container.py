
from PySide import QtCore, QtGui

class Container(QtGui.QWidget):
    def __init__(self, closeCallback, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMinimumSize(1000,200)
        self.ccb = closeCallback

    def closeEvent(self, event):
        self.ccb()