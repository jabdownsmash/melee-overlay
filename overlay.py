
import sys,os
import math
import random
from PySide import QtCore, QtGui
from p3.state_manager import StateManager
from p3.state import State, Menu
from p3.memory_watcher import MemoryWatcher
from overlay_widgets.components import FrameIndicator 

class Container(QtGui.QWidget):
    def __init__(self, board, closeCallback, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMinimumSize(1000,200)
        quit = QtGui.QPushButton("Calibrate")
        quit.resize(75, 30)
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        def buttonCB():
            board.calibrating = 2

        QtCore.QObject.connect(quit, QtCore.SIGNAL("clicked()"),buttonCB)
        quit.show()
        board.show()
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(quit, 0, 0)
        # gridLayout.addWidget(frameIndicator, 0, 1)
        gridLayout.addWidget(board, 1, 0, 2, 2)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)
        # self.addWidget(frameIndicator)
        # self.show()
        self.ccb = closeCallback

    def closeEvent(self, event):
        self.ccb()

class Melee(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

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
            print("x: " + str(x) + " y: " + str(y))
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


class Overlay():
    def __init__(self):

        if len(sys.argv) != 2:
            sys.exit('Usage: ' + sys.argv[0] + ' dolphin-home')
        home = sys.argv[1]

        self.state = State()
        sm = StateManager(self.state)

        # state.players[0].hitlag_counter_changed.append(listener)

        locationsTxt = ''
        for i in sm.locations():
            locationsTxt += i + '\n'

        with open(home + '/MemoryWatcher/Locations.txt', 'w') as file:
            file.write(locationsTxt)

        done = False

        def exitHandler():
            nonlocal done
            done = True

        app = QtGui.QApplication(sys.argv)

        self.board = Melee()
        self.newFI = True

        # fi = FrameIndicator()
        # fi.center = 0
        self.state.players[0].vertical_velocity_changed.append(self.listener)

        self.cont = Container(self.board, exitHandler)
        self.cont.show()
        self.fis = []
        self.state.frame_changed.append(self.listener2)
        # board.texts.append((200,350,"hello"))

        mww = MemoryWatcher(home + '/MemoryWatcher/MemoryWatcher')
        for returnValue in mww:
            if returnValue is not None:
                address, value = returnValue
                sm.handle(address,value)
            app.processEvents()
            if done:
                break

    def listener2 (self,state):
        for fi in self.fis:
            fi.alpha -= .002
            if fi.alpha < 0:
                fi.alpha = 0
            fi.update()

    def listener (self,state):
        # print(str(state.players[0].action_state) + " " + str(state.players[0].fastfall_velocity) + " " + str(state.players[0].vertical_velocity))
        if state.players[0].vertical_velocity < 0 and state.players[0].vertical_velocity + state.players[0].fastfall_velocity > 0:
            if self.newFI:
                self.newFI = False
                self.fi = FrameIndicator()

                self.fi.setParent(self.cont)
                self.fi.show()
                self.fi.center = 0

                # self.fi.move(100,200)
                self.fi.resize(80,8)
            self.fi.frameCounter += 1
            self.fi.setFrame(self.fi.frameCounter)


            x,y = self.board.transformPoint(state.players[0].x,-(state.players[0].y + 10))
            self.fi.move(x  - self.fi.width()/2,y)
        else:
            self.newFI = True
            try:
                self.fis.append(self.fi)
            except AttributeError:
                pass

if __name__ == '__main__':
    Overlay()
