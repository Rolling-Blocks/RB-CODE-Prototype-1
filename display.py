import random
import time
from disp_def import DispDef as DD
from disp_def import blockStateKey
import copy

class display:
    def __init__(self, dispDim, blockSide, lockSide, pixelKey, title = ""):
        
        # numLockRow ~ Height of Diplay
        self.numLockRow = dispDim[1]
        self.numBlockCol = dispDim[0]
        self.lockSide = lockSide
        self.blockSide = blockSide

        # Pixel Color
        self.pixelKey = pixelKey

        # Title
        self.title = title

        # state of virtual display stored as cube positions 0-3, position corresponds to color in location in pixelcolors
        self.displayState = [[0]*self.numBlockCol for i in range(self.numLockRow)]
        
        #states of locks unlocked/locked
        self.lockServoState = [DD.UNLOCK]*self.numLockRow

        # display viewer setup
        self.blockServoState = [DD.MIDDLE]*self.numBlockCol

    def getDisplayState(self):  return self.displayState
    
    def getBlockServoState(self, col = -1):
        if col < 0:
            return self.blockServoState
        else:
            return self.blockServoState[col]

    def getLockServoState(self, row = -1):          
        if row < 0:
            return self.lockServoState
        else:
            return self.lockServoState[row]

    def getTitle(self):             return self.title
    def getPixelKey(self):          return self.pixelKey
    def getDispDim(self):           return [self.numBlockCol, self.numLockRow]
    def getLockBankLocation(self):  return self.lockSide
    def getBlockBankLocation(self): return self.blockSide

    def setLockServo(self, row, state):     self.lockServoState[row] = state
    def setBlockServo(self, column, state):
        #print('initial: ' + str(blockStateKey(self.blockServoState[column])) + '  final' + str(blockStateKey(state)))
        columnChange = blockStateKey(state) - blockStateKey(self.blockServoState[column])
        self.blockServoState[column] = state
        for y in range(0,len(self.displayState)):
            if self.lockServoState[y] is DD.UNLOCK:
                self.displayState[y][column] = (self.displayState[y][column] + columnChange) % 4

    #prints displat as a 2d array of int values
    def printDispVal(self): 
        for s in self.displayState: 
            print(s)

    def sendGcode(self, arr):
        arrCop = copy.deepcopy(arr)
        moveType = arrCop.pop(0)
        moves = arrCop.pop(0)

        # Set Servo Positions
        if moveType is DD.ROWLOCK or moveType is DD.ROWUNLOCK:
            if len(moves) == self.numLockRow:
                for j in range(len(moves)):
                    self.setLockServo(j, moves[j], False)
        elif moveType is DD.COLRETURN or moveType is DD.COLACTUATE:
            if len(moves) == self.numBlockCol:
                for i in range(len(moves)):
                    self.setBlockServo(i, moves[i], False)

if __name__ == '__main__':
    dispDimensions = (16, 16) # (width, height)
    pixelKey = ('#080808','#404040','#B0B0B0','#FFFFFF')
    disp = display(dispDimensions, DD.TOP, DD.RIGHT, pixelKey)
    for i in range(0,dispDimensions[1]):
        disp.setLockServo(i, DD.LOCK)

    i = 1
    while True:
        x = random.randint(0,dispDimensions[0]-1)
        y = random.randint(0,dispDimensions[1]-1)

        disp.setLockServo(y, DD.UNLOCK)
        disp.setBlockServo(x, DD.ADD)
        disp.setLockServo(y, DD.LOCK)
        disp.setBlockServo(x, DD.MIDDLE)
        disp.printDispVal()
        print()
        time.sleep(2)

