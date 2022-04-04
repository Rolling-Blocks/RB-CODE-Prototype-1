import random
import time
from disp_def import DispDef as DD
from disp_def import blockStateKey
import copy
import json
import write_servo as ws

defaultTimesPerMove = {DD.ROWLOCK: 750, DD.COLRETURN: 1000, DD.ROWUNLOCK: 750, DD.COLACTUATE: 1000}

class display_real:
    def __init__(self, displayTitle, dsd, dispDim, blockSide = DD.TOP, lockSide = DD.RIGHT, pixelColors = 0, timePerMove = defaultTimesPerMove, raspi_channel = 1, module_IDs = [10, 14]):
        
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
        # display Servo Data, Contains Offset
        with open(dsd) as json_file:
            self.dispServoData = json.load(json_file)

        # state of virtual display stored as cube positions 0-3, position corresponds to color in location in pixelcolors
        self.displayState = [[0]*self.numBlockCol for i in range(self.numLockRow)]
        
        #states of locks unlocked/locked
        self.lockServoState = [DD.UNLOCK] * self.numLockRow

        # display viewer setup
        self.blockServoState = [DD.MIDDLE] * self.numBlockCol

        # Servo and Module Setup
        self.raspi_channel = raspi_channel
        self.module_IDs = module_IDs
        self.servos = ws.write_servo(module_IDs)

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

    def __getJsonValue(self, servoType, servoCoordinate, info):
        index = ""
        if servoType is DD.LOCK_SERVO:
            index += "r"
        if servoType is DD.BLOCK_SERVO:
            index += "c"
        index += str(servoCoordinate)

        print()
        print("__getJsonValue")
        print(index)
        print(str(info))
        got = self.dispServoData[index][info]
        print(got)

        return got

    # Returns
        # Desired Servo Set Position
    def __getDesServoPos(self, servoType, servoCoordinate, servoState):
        """
            servoType       [DD.LOCK or DD.BLOCK]
            servoCoordinate [int] x position or y postion of servo
        """
        # print stuffs
        print()
        print("__getServoSendTo")
        print(servoType)
        print(servoCoordinate)
        # Takes 
            # Lock or Block, 
            # Servo Coordinate location is 
            # Servo Desired state.
            # Handles what sides servos are on
            # Handles Offset of Where Servos Should 
        # Returns
            # Your Mom
            # Servo Set Position
        if not self.__getServoSendTo_InputChecker(servoType, servoCoordinate, servoSetPos):
            return False

        # Get Index of Servo for JSON
        write = self.__getJsonValue(servoType, servoCoordinate, 'centerOffset')

        # If you have to flip the servo position
        multiplier = 1
        if servoType is DD.LOCK_SERVO: 
            if servoSetPos is DD.LOCK:
                write += 255
            if servoSetPos is DD.UNLOCK:
                write += 128

        if servoType is DD.BLOCK_SERVO:
            if self.servoSetPos is DD.SUBTRACT:
                write += 255
            if self.servoSetPos is DD.MIDDLE:
                write += 127                
            if self.servoSetPos is DD.ADD:
                write += 0
        
        # compensate if the servo direction needs to be flipped
        if self.lockSide is DD.LEFT or self.lockSide is DD.BOTTOM:
            print("reversed")
            write = 255 - write

        # bounds the servo value to something that can be sent
        write = self.__bound(0, write, 255)

        return write
    
    def __getDesServoPos_InputChecker(self, servoType, servoCoordinate, servoState):
        # Checks for __getDesServoPos
        if servoType is not DD.LOCK_SERVO and servoType is not DD.BLOCK_SERVO:
            print("'__getDesServoPos' not given valid 'servoType' ")
            return False

        # Check BLOCK_SERVO is valid
        if servoType is DD.BLOCK_SERVO:
            # Check Valid 'servoCoordinate'
            if not (0 <= servoCoordinate) or not (servoCoordinate < self.numBlockCol):
                print("'servoCoordinate' for row is our of bounds")
                return False
            if not (servoState is DD.SUBTRACT or servoState is DD.MIDDLE or servoState is DD.ADD):
                print("'servoSetPos' state is not valid")
                return False

        # Check LOCK_SERVO is valid    
        if servoType is DD.LOCK_SERVO:
            # Check Valid 'servoCoordinate'
            if not (0 <= servoCoordinate) or not (servoCoordinate < self.numLockRow):
                print("'servoCoordinate' for row is our of bounds")
                return False
            if not (servoState is DD.LOCK or servoState is DD.UNLOCK):
                print("'servoSetPos' state is not valid")
                return False

        # Everything is Valid
        return True

    def __bound(self, low, high, value):
        return max(low, min(high, value))
    
    def setServo(self, st, sc, state):
        # Get Data for Write_Display
        moduleId    = self.__getJsonValue(servoType = st, servoCoordinate = sc, info = 'moduleId')
        servoId     = self.__getJsonValue(servoType = st, servoCoordinate = sc, info = 'servoId')
        offset      = self.__getJsonValue(servoType = st, servoCoordinate = sc, info = 'centerOffset')
        setPoint    = self.__getDesServoPos(servoType = st, servoCoordinate = sc, servoSetPos = state)
        
        # Updating Display Logged Locked States
        self.lockServoState[row] = state
        
        # Sending Data to Write_Display
        self.servos.setServo(moduleId, servoId, setPoint)

        # Update Display
        if updateAfter:
            self.servos.write_servos()

        # Return Time Needed for Move to Happen
        return timeForMove  

    def setLockServo(self, row, state, timeForMove = 1.000, updateAfter = True):
        """
            row         [int]
            state       [DD.LOCK or DD.UNLOCK]
            timeForMove [float]
        """
        # Get Data for Write_Display
        moduleId    = self.__getJsonValue(servoType = DD.LOCK_SERVO, servoCoordinate = row, info = 'moduleId')
        servoId     = self.__getJsonValue(servoType = DD.LOCK_SERVO, servoCoordinate = row, info = 'servoId')
        setPoint    = self.__getDesServoPos(servoType = DD.LOCK_SERVO, servoCoordinate = row, servoSetPos = state)
        
        # Updating Display Logged Locked States
        self.lockServoState[row] = state
        
        # Sending Data to Write_Display
        self.servos.setServo(moduleId, servoId, setPoint)

        # Update Display
        if updateAfter:
            self.servos.write_servos()

        # Return Time Needed for Move to Happen
        return timeForMove

    def setBlockServo(self, column, state, timeForMove = 1.000, updateAfter = True):
        """
            column      [int]
            state       [DD.SUBTRACT or DD.MIDDLE or DD.ADD]
            timeForMove [float]
        """
        # Get Data for Write_Display
        moduleID        = self.__getJsonValue(servoType = DD.BLOCK_SERVO, servoCoordinate = column, info = 'moduleId')
        servoModuleID   = self.__getJsonValue(servoType = DD.BLOCK_SERVO, servoCoordinate = column, info = 'servoId')
        setPoint        = self.__getDesServoPos(servoType = DD.BLOCK_SERVO, servoCoordinate = column, servoSetPos = state)

        # Updating Display Logged Block States
        self.blockServoState[column] = state

        # Update Pixel States
        columnChange = blockStateKey(state) - blockStateKey(self.blockServoState[column])
        self.blockServoState[column] = state
        for y in range(len(self.displayState)):
            if self.lockServoState[y] is DD.UNLOCK:
                self.displayState[y][column] = (self.displayState[y][column] + columnChange) % 4

        # Sending Data to Write_Display
        self.servos.setServo(moduleID, servoModuleID, setPoint)

        # Update Display
        if updateAfter:
            self.servos.write_servos()

        return timeForMove

        pass

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
    displayTit = '6x9 test'
    servoJson = 'display_16x16.json'
    dispDimensions = (16, 16) # (width, height)
    pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
    disp = display_real(displayTit, servoJson, dispDimensions, DD.TOP, DD.RIGHT, pixelVal) 

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

    