
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


        #p3 setup stuff
        if len(sys.argv) != 2:
            sys.exit('Usage: ' + sys.argv[0] + ' dolphin-home')
        home = sys.argv[1]

        locationsTxt = ''
        for i in sm.locations():
            locationsTxt += i + '\n'

        with open(home + '/MemoryWatcher/Locations.txt', 'w') as file:
            file.write(locationsTxt)

        self.state = State()
        sm = StateManager(self.state)

        #qt stuff
        app = QtGui.QApplication(sys.argv)

        #some vars
        self.newFI = True
        done = False
        def exitHandler():
            nonlocal done
            done = True

        #create container
        self.cont = Container(exitHandler)
        self.cont.show()

        #spawn fastfall counter
        fi = FastFallCounter(self.state)

        fi.setParent(self.cont)
        fi.show()
        fi.resize(1000,100)

        #p3 run loop
        mww = MemoryWatcher(home + '/MemoryWatcher/MemoryWatcher')
        for returnValue in mww:
            if returnValue is not None:
                address, value = returnValue
                sm.handle(address,value)
            app.processEvents()
            if done:
                break

if __name__ == '__main__':
    Overlay()
