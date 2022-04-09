import display_virtual_window as dvw
import random
import time
from disp_def import DispDef as DD
from disp_def import blockStateKey
import copy
import display as d

defaultTimesPerMove = {DD.ROWLOCK: 750, DD.COLRETURN: 1000, DD.ROWUNLOCK: 750, DD.COLACTUATE: 1000}

class display_virtual:
    def __init__(self, display, timePerMove = defaultTimesPerMove):
        self.display = display
        self.wind = dvw.display_virtual_window(display)
        # timePerMove is the time buffer corresponding to each time delay
        self.timePerMove = timePerMove

    def getDisplayState(self):              return self.display.getDisplayState()
    def getBlockServoPos(self, col = -1):   return self.display.getBlockServoState(col)
    def getLockServoPos(self, row = -1):    return self.display.getLockServoState(row)
    def refreshDisp(self):                  self.wind.updateDisplay()

    def setLockServo(self, row, state, dorefreshDisp = True):
        self.display.setLockServo(row, state)
        if dorefreshDisp:
            self.refreshDisp()
    def setBlockServo(self, col, state, dorefreshDisp = True):
        self.display.setBlockServo(col, state)
        if dorefreshDisp:
            self.refreshDisp()
    def printDispVal(self):
        #prints displat as a 2d array of int values
        for s in self.getDisplayState():
            print(s)
    
    ## sentGcode
        # sentGcode takes in gcode command, 
    def sendGcode(self, arr):
        self.display.sendGcode(arr)
        self.refreshDisp()

        # Send Back Time Buffer Required To Let Display Finish Move 
        return self.timePerMove[arr[0]]

if __name__ == '__main__':
    display = d.display((16, 16), DD.TOP, DD.RIGHT, ('#080808','#404040','#B0B0B0','#FFFFFF'), '16x16 display_virtual test')
    virtDisp = display_virtual(display)  
    virtDisp.printDispVal()
    dispDimensions = display.getDispDim()
    for i in range(0,dispDimensions[1]):
        display.setLockServo(i, DD.LOCK)
    virtDisp.refreshDisp()

    i = 1
    while True:
        x = random.randint(0,dispDimensions[0]-1)
        y = random.randint(0,dispDimensions[1]-1)
        t = 0.01

        display.setLockServo(y, DD.UNLOCK)
        virtDisp.refreshDisp()
        time.sleep(t)

        display.setBlockServo(x, DD.ADD)
        virtDisp.refreshDisp()
        time.sleep(t)
        
        display.setLockServo(y, DD.LOCK)
        virtDisp.refreshDisp()
        time.sleep(t)

        display.setBlockServo(x, DD.MIDDLE)
        virtDisp.refreshDisp()
        time.sleep(t)
