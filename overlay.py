
import sys,os
import math
import random
from PySide import QtCore, QtGui
from p3.state_manager import StateManager
from p3.state import State, Menu
from p3.memory_watcher import MemoryWatcher
from overlay_widgets.components import FrameIndicator 
from overlay_widgets.fastfall_counter import FastFallCounter
from screens.calibration import Calibration
from container import Container

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

        # self.board = Melee()
        self.newFI = True

        # fi = FrameIndicator()
        # fi.center = 0
        # self.state.players[0].vertical_velocity_changed.append(self.listener)

        self.cont = Container(exitHandler)
        self.cont.show()


        fi = FastFallCounter(self.state)

        fi.setParent(self.cont)
        fi.show()
        fi.resize(1000,100)

        # fi.move(100,200)
        # self.state.frame_changed.append(self.listener2)
        # board.texts.append((200,350,"hello"))

        mww = MemoryWatcher(home + '/MemoryWatcher/MemoryWatcher')
        for returnValue in mww:
            if returnValue is not None:
                address, value = returnValue
                sm.handle(address,value)
            app.processEvents()
            if done:
                break

    # def listener2 (self,state):
    #     for fi in self.fis:
    #         fi.alpha -= .002
    #         if fi.alpha < 0:
    #             fi.alpha = 0
    #         fi.update()

    # def listener (self,state):
    #     # print(str(state.players[0].action_state) + " " + str(state.players[0].fastfall_velocity) + " " + str(state.players[0].vertical_velocity))
    #     if state.players[0].vertical_velocity < 0 and state.players[0].vertical_velocity + state.players[0].fastfall_velocity > 0:
    #         if self.newFI:
    #             self.newFI = False
    #             self.fi = FrameIndicator()

    #             self.fi.setParent(self.cont)
    #             self.fi.center = 0
    #             self.fi.resize(80,8)
    #             self.fi.show()

    #             # self.fi.move(100,200)
    #         self.fi.frameCounter += 1
    #         self.fi.setFrame(self.fi.frameCounter)


    #         x,y = self.board.transformPoint(state.players[0].x,-(state.players[0].y + 10))
    #         self.fi.move(x  - self.fi.width()/2,y)
    #     else:
    #         self.newFI = True
    #         try:
    #             self.fis.append(self.fi)
    #         except AttributeError:
    #             pass

if __name__ == '__main__':
    Overlay()
