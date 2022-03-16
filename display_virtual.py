import display_virtual_window as dvw
import random
import time
from disp_def import DispDef as DD
from disp_def import blockStateKey
import copy

defaultTimesPerMove = {DD.ROWLOCK: 750, DD.COLRETURN: 1000, DD.ROWUNLOCK: 750, DD.COLACTUATE: 1000}

class display_virtual:
    def __init__(self, displayTitle, dispDim, blockSide, lockSide, pixelColors, timePerMove = defaultTimesPerMove):
        
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
        # timePerMove is the time buffer corresponding to each time delay
        self.timePerMove = timePerMove

        # state of virtual display stored as cube positions 0-3, position corresponds to color in location in pixelcolors
        self.displayState = [[0]*self.numBlockCol for i in range(self.numLockRow)]
        
        #states of locks unlocked/locked
        self.lockServoState = [DD.UNLOCK]*self.numLockRow

        # display viewer setup
        self.blockServoState = [DD.MIDDLE]*self.numBlockCol

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

    def setLockServo(self, row, state, doUpdateDisp = True):
        self.lockServoState[row] = state
        if doUpdateDisp:
            self.updateDisp()
      
    def setBlockServo(self, column, state, doUpdateDisp = True):
        #print('initial: ' + str(blockStateKey(self.blockServoState[column])) + '  final' + str(blockStateKey(state)))
        columnChange = blockStateKey(state) - blockStateKey(self.blockServoState[column])
        self.blockServoState[column] = state
        for y in range(0,len(self.displayState)):
            if self.lockServoState[y] is DD.UNLOCK:
                self.displayState[y][column] = (self.displayState[y][column] + columnChange) % 4
        if doUpdateDisp:
            self.updateDisp()

    ## sentGcode
        # sentGcode takes in gcode command, 
    def sendGcode(self, arr):
        arrCop = copy.deepcopy(arr)
        moveType = arrCop.pop(0)
        moves = arrCop.pop(0)

        # Set Servo Positions
        if moveType is DD.ROWLOCK or moveType is DD.ROWUNLOCK:
            if not len(moves) == self.numLockRow:
                print("Gcode Command Sent Incorrect Number of Servo Commands")
                print("Expected " + str(self.numLockRow) + ", Recieved " + str(len(moves)))
            else:
                print("Running Lock Actuation")
                for j in range(len(moves)):
                    self.setLockServo(j, moves[j], False)
        elif moveType is DD.COLRETURN or moveType is DD.COLACTUATE:
            if not len(moves) == self.numBlockCol:
                print("Gcode Command Sent Incorrect Number of Servo Commands")
                print("Expected " + str(self.numBlockCol) + ", Recieved " + str(len(moves)))
            else:
                print("Running Block Actuation")
                for i in range(len(moves)):
                    self.setBlockServo(i, moves[i], False)
        self.updateDisp()

        # Send Back Time Buffer Required To Let Display Finish Move 
        return self.timePerMove[moveType]

    #prints displat as a 2d array of int values
    def printDispVal(self):
        for s in self.displayState:
            print(s)

    def updateDisp(self):
        self.wind.setFrameLocks(self.displayState, self.lockServoState, self.blockServoState)

if __name__ == '__main__':
    dispDimensions = (16, 16) # (width, height)
    pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
    displayTit = '6x9 test'
    disp = display_virtual(displayTit, dispDimensions, DD.TOP, DD.RIGHT, pixelVal)  
    disp.printDispVal()
    for i in range(0,dispDimensions[1]):
        disp.setLockServo(i, DD.LOCK)
    disp.updateDisp()

    i = 1
    while True:
        x = random.randint(0,dispDimensions[0]-1)
        y = random.randint(0,dispDimensions[1]-1)
        t = 0.01

        disp.setLockServo(y, DD.UNLOCK)
        disp.updateDisp()
        time.sleep(t)

        disp.setBlockServo(x, DD.ADD)
        disp.updateDisp()
        time.sleep(t)
        
        disp.setLockServo(y, DD.LOCK)
        disp.updateDisp()
        time.sleep(t)

        disp.setBlockServo(x, DD.MIDDLE)
        disp.updateDisp()
        time.sleep(t)
