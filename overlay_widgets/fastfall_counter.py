
from PySide import QtCore, QtGui
from overlay_widgets.components import FrameIndicator

class FastFallCounter(QtGui.QWidget):

    def __init__(self, state, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMinimumSize(80,8)

        self.fi = FrameIndicator()

        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(self.fi, 0, 0)
        self.fi.show()
        self.fi.center = 0
        self.frameCounter = 0
        self.oneShot = False
        self.newFI = False
        # gridLayout.addWidget(frameIndicator, 0, 1)
        # gridLayout.addWidget(board, 1, 0, 2, 2)
        # gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)
        # self.addWidget(frameIndicator)
        # self.show()
        state.players[0].vertical_velocity_changed.append(self.listener)

    def listener (self,state):
        # print(str(state.players[0].action_state) + " " + str(state.players[0].fastfall_velocity) + " " + str(state.players[0].vertical_velocity))
        if state.players[0].vertical_velocity < 0 and state.players[0].vertical_velocity + state.players[0].fastfall_velocity > 0:
            if not (self.newFI and self.oneShot):
                if self.newFI:
                    self.frameCounter = 0
                    self.newFI = False
                else:
                    self.frameCounter += 1
                self.fi.setFrame(self.frameCounter)
        else:
            self.newFI = True
