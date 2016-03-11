
import sys,os
import math
import random
from PySide import QtCore, QtGui
from p3.state_manager import StateManager
from p3.state import State, Menu
from p3.memory_watcher import MemoryWatcher
from transitions import Machine

class Container(QtGui.QWidget):
    def __init__(self, board, closeCallback, frameIndicator, parent=None):
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
        # quit.show()
        # board.show()
        gridLayout = QtGui.QGridLayout()
        # gridLayout.addWidget(quit, 0, 0)
        gridLayout.addWidget(frameIndicator, 0, 1)
        # gridLayout.addWidget(board, 1, 0, 2, 2)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)
        # self.show()
        self.ccb = closeCallback

    def closeEvent(self, event):
        self.ccb()

class FrameIndicator(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.frame = 0
        self.numFrames = 7
        self.frameCounter = -1
        self.center = (self.numFrames - 1)/2

        self.machine = Machine(model=self, states=['blank','show'], initial='blank')
        self.machine.add_transition(trigger='setFrame', source=['blank','show'], dest='show', before='setRects')

    def setRects(self,frame):
        self.frame = frame
        self.update()

    def paintEvent(self,event):
        painter = QtGui.QPainter(self)

        for i in range(self.numFrames):
            if self.state == 'blank':
                painter.setPen(QtGui.QColor(55,55,55,255))
                painter.setBrush(QtGui.QColor(55,55,55,255))
            else: 
                if (i == 0 and self.frame <= -self.center and self.center > 0) or (i - self.center == self.frame and self.frame < 0):
                    painter.setPen(QtGui.QColor(55,55,255,255))
                    painter.setBrush(QtGui.QColor(55,55,255,255))
                elif ((i == self.numFrames - 1) and (self.frame >= self.numFrames - self.center) and self.center < (self.numFrames - 1)) or (i - self.center == self.frame and self.frame > 0):
                    painter.setPen(QtGui.QColor(255,55,55,255))
                    painter.setBrush(QtGui.QColor(255,55,55,255))
                elif self.frame == 0 and i == self.center:
                    painter.setPen(QtGui.QColor(255,255,255,255))
                    painter.setBrush(QtGui.QColor(255,255,255,255))
                else:
                    painter.setPen(QtGui.QColor(55,55,55,255))
                    painter.setBrush(QtGui.QColor(55,55,55,255))
            # painter.drawRect(QtCore.QRect(0, i * self.height()/self.numFrames, self.width(), self.height()/self.numFrames - self.height()/21))
            painter.drawRect(QtCore.QRect(i * self.width()/self.numFrames, 0, self.width()/self.numFrames - self.width()/21, self.height() - 1))


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


    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        scale = (self.x2 - self.x1)/(88.47*2)
        xOffset = self.x1 + (self.x2 - self.x1)/2
        yOffset = (self.y1 + self.y2)/2

        for text in self.texts:
            painter.setPen(QtCore.Qt.white)
            painter.setFont(QtGui.QFont("Courier", 20, QtGui.QFont.Bold))
            painter.save()
            painter.translate(text[0]*scale + xOffset, text[1]*scale + yOffset)
            painter.drawText(self.rect(), text[2])
            painter.restore()

        for rect in self.rectangles:
            painter.setPen(QtCore.Qt.white)
            painter.setBrush(QtGui.QColor(*rect[4]))
            painter.drawRect(QtCore.QRect(rect[0]*scale + xOffset - rect[2]/2, -rect[1]*scale + yOffset - rect[3]/2, rect[2], rect[3]))

        # painter.setPen(QtCore.Qt.NoPen)
        # painter.setBrush(QtCore.Qt.blue)
        # painter.save()
        # painter.translate(0, self.height())
        # painter.drawPie(QtCore.QRect(-35, -35, 70, 70), 0, 90 * 16)
        # painter.restore()

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

def listener (state,fi):
    # print(str(state.players[0].action_state) + " " + str(state.players[0].fastfall_velocity) + " " + str(state.players[0].vertical_velocity))
    if state.players[0].vertical_velocity < 0 and state.players[0].vertical_velocity + state.players[0].fastfall_velocity > 0:
        fi.frameCounter += 1
        fi.setFrame(fi.frameCounter)
    else:
        fi.frameCounter = -1

def start(setup):

    if len(sys.argv) != 2:
        sys.exit('Usage: ' + sys.argv[0] + ' dolphin-home')
    home = sys.argv[1]

    state = State()
    sm = StateManager(state)

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

    board = Melee()

    fi = FrameIndicator()
    fi.center = 0
    state.players[0].vertical_velocity_changed.append(lambda x: listener(x,fi))

    cont = Container(board, exitHandler,fi)
    cont.show()
    setup(state,board,cont)
    # board.texts.append((200,350,"hello"))

    mww = MemoryWatcher(home + '/MemoryWatcher/MemoryWatcher')
    for returnValue in mww:
        if returnValue is not None:
            address, value = returnValue
            sm.handle(address,value)
        app.processEvents()
        if done:
            break

# sys.exit(app.exec_())
def zoxx(state,board,cont):
    kek = [300,400,100,100,(255,0,0,60)]
    board.rectangles.append(kek)

    def listener2 (state):
        if state.menu == Menu.Game:
            kek[0] = state.players[0].x
            kek[1] = state.players[0].y
            board.update()
    state.frame_changed.append(listener2)
    # state.players[0].x_changed.append(listener2)

if __name__ == '__main__':
    start(zoxx)
