import display_virtual_window
import random
import time
from disp_def import DispDef, blockStateKey

class display_virtual:
    def __init__(self, displayTitle, numBlockCol, blockSide, numLockRow, lockSide, pixelColors):
        self.wind = display_virtual_window.display_virtual_window(displayTitle, numBlockCol, blockSide, numLockRow, lockSide, pixelColors)
        # numLockRow ~ Height of Diplay
        self.numLockRow = numLockRow
        # lockSide ~ left/right
        self.lockSide = lockSide
        # numBlockCol ~ width of Diplay
        self.numBlockCol = numBlockCol
        # blockSide ~ top/bottom
        self.blockSide = blockSide
        # pixelColors (pixelcolor0,pixelcolor1,pixelcolor2,pixelcolor3) pixel color values  
        self.pixelColors = pixelColors

        # state of virtual display stored as cube positions 0-3, position corresponds to color in location in pixelcolors
        self.displayState = [[0]*numBlockCol for i in range(numLockRow)]
        
        #states of locks unlocked/locked
        self.lockServoState = [DispDef.UNLOCK]*numLockRow

        # display viewer setup
        self.blockServoState = [DispDef.MIDDLE]*numBlockCol

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
        columnChange = blockStateKey(state) - blockStateKey(self.lockServoState[column])
        self.blockServoState[column] = state
        for y in range(0,len(self.displayState)):
            if self.lockServoState[y] is DispDef.UNLOCK:
                self.displayState[y][column] = (self.displayState[column][y] + columnChange) % 4
        self.updateDisp()

    #prints displat as a 2d array of int values
    def printDispVal(self):
        for s in self.displayState:
            print(s)

    def updateDisp(self):
        self.wind.newFrame(self.displayState, self.lockServoState, self.blockServoState)

if __name__ == '__main__':
    dispDimensions = (16, 16)
    disp = display_virtual('6x9 test', dispDimensions[0], DispDef.TOP,  dispDimensions[1], DispDef.RIGHT,('#042940','#005C53','#9FC131','#DBF227'))  
    for i in range(0,16):
        disp.setLockServo(i, DispDef.LOCK)
    disp.updateDisp()

    i = 1
    while True:
        x = random.randint(0,dispDimensions[0]-1)
        y = random.randint(0,dispDimensions[1]-1)
        
        t = 0.05

        disp.setLockServo(y, DispDef.UNLOCK)
        time.sleep(t)

        disp.setBlockServo(x, DispDef.ADD)
        time.sleep(t)
        
        disp.setLockServo(y, DispDef.LOCK)
        time.sleep(t)

        disp.setBlockServo(x, DispDef.MIDDLE)
        time.sleep(t)
        #print(i)