import display_virtual_window as dvw
import random
import time
from disp_def import DispDef, blockStateKey

class display_virtual:
    def __init__(self, displayTitle, dispDim, blockSide, lockSide, pixelColors):
        self.wind = dvw.display_virtual_window(displayTitle, dispDim, blockSide, lockSide, pixelColors)
        # numLockRow ~ Height of Diplay
        self.numLockRow = dispDim[1]
        # lockSide ~ left/right
        self.lockSide = lockSide
        # numBlockCol ~ width of Diplay
        self.numBlockCol = dispDim[0]
        # blockSide ~ top/bottom
        self.blockSide = blockSide
        # pixelColors (pixelcolor0,pixelcolor1,pixelcolor2,pixelcolor3) pixel color values  
        self.pixelColors = pixelColors

        # state of virtual display stored as cube positions 0-3, position corresponds to color in location in pixelcolors
        self.displayState = [[0]*self.numBlockCol for i in range(self.numLockRow)]
        
        #states of locks unlocked/locked
        self.lockServoState = [DispDef.UNLOCK]*self.numLockRow

        # display viewer setup
        self.blockServoState = [DispDef.MIDDLE]*self.numBlockCol

    def getPixelKey(self):
        return self.pixelColors

    def getDisplayState(self):
        return self.displayState

    def getBlockServoPos(self):
        return self.blockServoState

    def getBlockServoPos(self, col):
        return self.blockServoState[col]

    def getLockServoPos(self):
        return self.lockServoState

    def getLockServoPos(self, row):
        return self.lockServoState[row]

    def setLockServo(self, row, state):
        self.lockServoState[row] = state
        self.updateDisp()
      
    def setBlockServo(self, column, state):
        #print('initial: ' + str(blockStateKey(self.blockServoState[column])) + '  final' + str(blockStateKey(state)))
        columnChange = blockStateKey(state) - blockStateKey(self.blockServoState[column])
        self.blockServoState[column] = state
        for y in range(0,len(self.displayState)):
            if self.lockServoState[y] is DispDef.UNLOCK:
                self.displayState[y][column] = (self.displayState[y][column] + columnChange) % 4
        self.updateDisp()

    #prints displat as a 2d array of int values
    def printDispVal(self):
        for s in self.displayState:
            print(s)

    def updateDisp(self):
        self.wind.newFrame(self.displayState, self.lockServoState, self.blockServoState)

if __name__ == '__main__':
    dispDimensions = (6, 6) # (width, height)
    pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
    displayTit = '6x9 test'
    disp = display_virtual(displayTit, dispDimensions, DispDef.TOP, DispDef.RIGHT, pixelVal)  
    disp.printDispVal()
    for i in range(0,dispDimensions[1]):
        disp.setLockServo(i, DispDef.LOCK)
    disp.updateDisp()

    i = 1
    while True:
        x = random.randint(0,dispDimensions[0]-1)
        y = random.randint(0,dispDimensions[1]-1)
        t = 0.01

        disp.setLockServo(y, DispDef.UNLOCK)
        disp.updateDisp()
        time.sleep(t)

        disp.setBlockServo(x, DispDef.ADD)
        disp.updateDisp()
        time.sleep(t)
        
        disp.setLockServo(y, DispDef.LOCK)
        disp.updateDisp()
        time.sleep(t)

        disp.setBlockServo(x, DispDef.MIDDLE)
        disp.updateDisp()
        time.sleep(t)
