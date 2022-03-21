import random
import time
from disp_def import DispDef as DD
from disp_def import blockStateKey
import copy

defaultTimesPerMove = {DD.ROWLOCK: 750, DD.COLRETURN: 1000, DD.ROWUNLOCK: 750, DD.COLACTUATE: 1000}

class display_real:
    def __init__(self, displayTitle, dispDim, blockSide = DD.TOP, lockSide = DD.RIGHT, pixelColors, timePerMove = defaultTimesPerMove):
        
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

    def __getServoSendTo(self, servoType = DD.LOCK, servoCoordinate = 0, servoSetPos):
        # Takes 
            # Lock or Block, 
            # Servo Coordinate location is 
            # Servo Desired state.
        # Handles what sides servos are on
        # Handles Offset of Where Servos Should 
        if not self.__getServoSendTo_InputChecker(self, servoType, servoCoordinate, servoSetPos):
            return False
            

    def __getServoSendTo_InputChecker(self, servoType, servoCoordinate, servoSetPos):
         # Checks for __getServoSendTo()
        if servoType is not DD.LOCK and servoType is not DD.BLOCK:
            print("'__getServoSendTo()' not given valid 'servoType' ")
            return False

        if servoType is DD.LOCK:
            # Check Valid 'servoCoordinate'
            if not (0 <= servoCoordinate) or not (servoCoordinate < self.numLockRow):
                print("'servoCoordinate' for row is our of bounds")
                return False
            if not (servoSetPos is DD.SUBTRACT or servoSetPos is DD.MIDDLE or servoSetPos is DD.ADD):
                print("'servoSetPos' state is not valid")
                return False
            
        if servoType is DD.LOCK:
            # Check Valid 'servoCoordinate'
            if not (0 <= servoCoordinate) or not (servoCoordinate < self.numLockRow):
                print("'servoCoordinate' for row is our of bounds")
                return False
            if not (servoSetPos is DD.SUBTRACT or servoSetPos is DD.MIDDLE or servoSetPos is DD.ADD):
                print("'servoSetPos' state is not valid")
                return False

        return True

    def setLockServo(self, row, state, timeForMove = 1.000):
        self.lockServoState[row] = state
        return timeForMove

      
    def setBlockServo(self, column, state):
        #print('initial: ' + str(blockStateKey(self.blockServoState[column])) + '  final' + str(blockStateKey(state)))
        columnChange = blockStateKey(state) - blockStateKey(self.blockServoState[column])
        self.blockServoState[column] = state
        for y in range(0,len(self.displayState)):
            if self.lockServoState[y] is DD.UNLOCK:
                self.displayState[y][column] = (self.displayState[y][column] + columnChange) % 4

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

        # Send Back Time Buffer Required To Let Display Finish Move 
        return self.timePerMove[moveType]

    #prints displat as a 2d array of int values
    def printDispVal(self):
        for s in self.displayState:
            print(s)

if __name__ == '__main__':
    dispDimensions = (16, 16) # (width, height)
    pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
    displayTit = '6x9 test'
    disp = display_real(displayTit, dispDimensions, DD.TOP, DD.RIGHT, pixelVal)  
    disp.printDispVal()
    for i in range(0,dispDimensions[1]):
        disp.setLockServo(i, DD.LOCK)

    i = 1
    while True:
        x = random.randint(0,dispDimensions[0]-1)
        y = random.randint(0,dispDimensions[1]-1)
        t = 0.75

        disp.setLockServo(y, DD.UNLOCK)
        time.sleep(t)

        disp.setBlockServo(x, DD.ADD)
        time.sleep(t)
        
        disp.setLockServo(y, DD.LOCK)
        time.sleep(t)

        disp.setBlockServo(x, DD.MIDDLE)
        time.sleep(t)
