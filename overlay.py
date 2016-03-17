
import sys,os
import math
import random
from PySide import QtCore, QtGui
from p3.state_manager import StateManager
from p3.state import State
from p3.memory_watcher import MemoryWatcher
from overlay_widgets.fastfall_counter import FastFallCounter
from container import Container

class Overlay():
    def __init__(self):


        #p3 setup stuff
        if len(sys.argv) != 2:
            sys.exit('Usage: ' + sys.argv[0] + ' dolphin-home')
        home = sys.argv[1]

        state = State()
        sm = StateManager(state)
        
        locationsTxt = ''
        for i in sm.locations():
            locationsTxt += i + '\n'

        with open(home + '/MemoryWatcher/Locations.txt', 'w') as file:
            file.write(locationsTxt)

        #qt stuff
        app = QtGui.QApplication(sys.argv)

        #handle closing
        done = False
        def exitHandler():
            nonlocal done
            done = True

        #create container
        cont = Container(exitHandler)
        cont.show()

        #spawn fastfall counter
        ffc = FastFallCounter(state)

        ffc.setParent(cont)
        ffc.show()
        ffc.resize(1000,100)

        #p3 run loop
        mw = MemoryWatcher(home + '/MemoryWatcher/MemoryWatcher')
        for returnValue in mw:
            if returnValue is not None:
                address, value = returnValue
                sm.handle(address,value)
            app.processEvents()
            if done:
                break

if __name__ == '__main__':
    Overlay()
