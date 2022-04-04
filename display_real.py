import random
import time
from disp_def import DispDef as DD
from disp_def import blockStateKey
import copy
import json
import write_servo as ws
import display_real_interface as dri

class display_real:
    def __init__(self, displayTitle, dispDim, interface, pixelColors, timePerMove):
        
        # numLockRow ~ Height of Diplay
        self.numLockRow = dispDim[1]
        # numBlockCol ~ width of Diplay
        self.numBlockCol = dispDim[0]
        # pixelColors (pixelcolor0,pixelcolor1,pixelcolor2,pixelcolor3) pixel color values  
        self.pixelColors = pixelColors
        # timePerMove is the time buffer corresponding to each time delay
        self.timePerMove = timePerMove

        # state of virtual display stored as cube positions 0-3, position corresponds to color in location in pixelcolors
        self.displayState = [[0]*self.numBlockCol for i in range(self.numLockRow)]
        self.lockServoState = [DD.UNLOCK] * self.numLockRow
        self.blockServoState = [DD.MIDDLE] * self.numBlockCol

        # Display Real Interface
        self.dispInterface = interface
        self.dispInterface.setLockServos(self.blockServoState)
        time.sleep(1)
        self.dispInterface.setBlockServos(self.blockServoState)

    def getPixelKey(self):              return self.pixelColors
    def getDisplayState(self):          return self.displayState
    def getBlockServosPos(self):        return self.dispInterface.getBlockServosPos(self)
    def getBlockServoPos(self, col):    return self.dispInterface.getBlockServoPos(self, col)
    def getLockServosPos(self):         return self.dispInterface.getLockServosPos(self)
    def getLockServoPos(self, row):     return self.dispInterface.getLockServoPos(self, row)
 
    def setLockServo(self, row, state, updateAfter = True):
        """
            row         [int]
            state       [DD.UNLOCK or DD.LOCK]
            updateAfter [boolean]
        """
        self.dispInterface.setLockServo(row, state, updateAfter)
        self.lockServoState[row] = state

    def setBlockServo(self, col, state, updateAfter = True):
        """
            col         [int]
            state       [DD.SUBTRACT or DD.MIDDLE or DD.ADD]
            updateAfter [boolean]
        """
        self.dispInterface.setLockServo(row, state, updateAfter)
        self.blockServoState[column] = state

        # Update Pixel States
        columnChange = blockStateKey(state) - blockStateKey(self.blockServoState[column])
        self.blockServoState[column] = state
        for y in range(len(self.displayState)):
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
    servoJson = 'display_16x16.json'
    dispDimensions = (16, 16) # (width, height)
    servoPm = spm.servo_packet_manager(module_IDs = [10, 14])
    dispInter = display_real_interface(servoJson, dispDimensions, DD.TOP, DD.RIGHT, servoPm) 
    
    displayTit = '6x9 test'
    pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
    timePerMove = {DD.ROWLOCK: 750, DD.COLRETURN: 1000, DD.ROWUNLOCK: 750, DD.COLACTUATE: 1000}
    disp = display_real(displayTitle = displayTit, dispDim = dispDimensions, interface = dispInter, pixelColors = pixelVal, timePerMove = timePerMove)
    # displayTitle, dispDim, interface, pixelColors, timePerMove  
    
    disp.printDispVal()

    while True:
        for i in range(dispDimensions[1]):
            disp.setLockServo(i, DD.LOCK)
        print("LOCK")
        time.sleep(2)

        for i in range(dispDimensions[1]):
            disp.setLockServo(i, DD.UNLOCK)
        print("UNLOCK")
        time.sleep(2)

    