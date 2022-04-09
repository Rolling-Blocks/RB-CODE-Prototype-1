import random
import time
from disp_def import DispDef as DD
from disp_def import blockStateKey
import copy
import json
import servo_packet_manager as spm
# Gets States and handles navigation of JSON and publishing to servos

class display_real_interface:
    def __init__(self, servoFile, dispDim, blockSide, lockSide, givenSpm = spm.servo_packet_manager([10,14])):
        
        # numLockRow ~ Height of Diplay
        self.numLockRow = dispDim[1]
        # lockSide ~ left/right
        self.lockSide = lockSide
        # numBlockCol ~ width of Diplay
        self.numBlockCol = dispDim[0]
        # blockSide ~ top/bottom
        self.blockSide = blockSide
        # display Servo Data, Contains Offset
        with open(servoFile) as json_file:
            self.dispServoData = json.load(json_file)

        #states of locks unlocked/locked
        self.lockServoState = [DD.UNLOCK] * self.numLockRow
        
        # display viewer setup
        self.blockServoState = [DD.MIDDLE] * self.numBlockCol

        self.servos = givenSpm
        self.setLockServos(self.lockServoState)
        self.setBlockServos(self.blockServoState)


    def getBlockServosState(self):          return self.blockServoState
    def getBlockServoState(self, col):      return self.blockServoState[col]
    def getLockServosState(self):           return self.lockServoState
    def getLockServoState(self, row):       return self.lockServoState[row]
    def updateServos(self):                 self.servos.write_servos()

    def __servoJsonInfo(self, servoType, servoCoordinate): # Written #Untested
        """
            servoType       DD.LOCK or DD.BLOCK
            servoCoordinate int
        """
        index = ""
        if servoType is DD.LOCK_SERVO:
            index += "r"
        if servoType is DD.BLOCK_SERVO:
            index += "c"
        index += str(servoCoordinate)

        #print()
        #print("__getJsonValue")
        #print(index)
        #print(str(info))
        modId   = self.dispServoData[index]["moduleId"]
        serId   = self.dispServoData[index]["servoId"] 
        cenOff  = self.dispServoData[index]["centerOffset"] 
        toRet = (modId, serId, cenOff)
        #print(toRet)
        return toRet

    # Turns ServoState To Default Servo Position, does not account for bay position
        # Does not handle for compensation of servo bay position
    def __getPosFromState(self, servoType, servoState): #WRITTEN #UNCHECKED
        """
            servoType   DD.LOCK or DD.BLOCK
            servoState  DD. (appropriate)
        """
        # Prints Error If Given Invalid Directions

        write = -1
        if servoType is DD.LOCK_SERVO: 
            if servoState is DD.LOCK:
                write = 255
            if servoState is DD.UNLOCK:
                write = 128

        if servoType is DD.BLOCK_SERVO:
            if servoState is DD.SUBTRACT:
                write = 255
            if servoState is DD.MIDDLE:
                write = 127                
            if servoState is DD.ADD:
                write = 0
        
        if write == -1:
            print("__getPosFromState given invalid servoType servoState combo")
            print("given ServoType" + str(servoType) + "   and ServoState " + str(servoState) )

        return write

    # Returns - absolute Servo Set Position
        # Compensates for Servo Offsets
        # Compensates for position of the servo array to reverse direction if appropriate
    def __bayCompensator(self, servoType, defaultServoPos, offset):
        # Note on Offsets
        # Pixel Adjustment 
            # LEFT/RIGHT is NEGATIVE/POSITIVE       ~ offsets
            # default 0 to 255 is right to left     ~ absolute
        # Lock Adjustment 
            # DOWN/UP is NEGATIVE/ POSITIVE         ~ offsets
            # default 0 to 255 is down to up        ~ absolute
        """
            servoType           DD.LOCK or DD.BLOCK
            defaultServoPos     int (between zero and 255)
            offset              absolute
        """
        write = -256
        # Do as if Default Config Bays Top and Right
        if servoType is DD.BLOCK_SERVO:
            write = defaultServoPos - offset
        elif servoType is DD.LOCK_SERVO:
            write = defaultServoPos + offset
        else:
            print("__bayCompensator " + "invalid servoType Given" + " ServoType:" + str(servoType))

        # bounds the servo value to something that can be sent
        #print("default position given " + str(defaultServoPos))
        #print("write before bounds " + str(write))
        write = self.__bound(0, write, 255)
        #print("write after bounds " + str(write))
        
        # Reverse if necessary
        if self.lockSide is DD.LEFT or self.lockSide is DD.BOTTOM:
            print("reversed")
            write = 255 - write

        return write
    
    def __bound(self, low, high, value): return max(low, min(high, value))

    # Updates Standard Packet To Be Sent
    def __setServo(self, st, sc, state):
        """
            st          DD.LOCK or DD.BLOCK
            sc          int (servocoordinate)
            state       DD. (appropriate)
        """
        # Get Data for Write_Display
        moduleId, servoId, offset = self.__servoJsonInfo(st, sc)
        # Get what ServoPosition would be if no offset and if servoBays in default places 
        defaultServoPos = self.__getPosFromState(servoType = st, servoState = state)
        #print("defaultServoPos givens ~  servoType:" + str(st) + "  servoState:" + str(state))

        toSendToServo = self.__bayCompensator(st, defaultServoPos, offset)

        # Update Logged Servo State
        self.lockServoState[sc] = state
        
        # Sending Data to Write_Display
        self.servos.setServo(moduleId, servoId, toSendToServo)
    
    # Write To Singular Row
    def setLockServo(self, row, state, updateAfter = True):
        """
            row         [int]
            state       [DD.LOCK or DD.UNLOCK]
        """
        self.__setServo(st = DD.LOCK_SERVO, sc = row, state = state)

        # Update Display
        if updateAfter:
            self.writeServos()

    # Write To Multiple Rows
    def setLockServos(self, states):
        """
            states      [DD.LOCK or DD.UNLOCK]   length same as number of rows
        """
        if not len(states) == self.numLockRow:
            print("setLockServos" + " given invalid number of servo states")
        else:
            for i in range(len(states)):
                self.setLockServo(i, states[i], updateAfter = False)
        self.writeServos()

    def writeServos(self):
        self.servos.write_servos()

    ### Copy For Columns once Lock Code Checked    
    def setBlockServo(self, col, state, updateAfter = True):
        """
            col         [int]
            state       DD.SUBTRACT or DD.MIDDLE or DD.ADD
        """
        self.__setServo(st = DD.BLOCK_SERVO, sc = col, state = state)

        # Update Display
        if updateAfter:
            self.writeServos()
    
    def setBlockServos(self, states):
        """
            states      [DD.SUBTRACT or DD.MIDDLE or DD.ADD]   length same as number of rows
        """
        if not len(states) == self.numBlockCol:
            print("setBlockServos" + " given invalid number of servo states")
        for i in range(len(states)):
            self.setBlockServo(i, states[i], updateAfter = False)
        self.writeServos()

    def __checkParametersValid(self, servoCoordinate, servoType, servoState):
        # Checks for __getDesServoPos
        if servoType is not DD.LOCK_SERVO and servoType is not DD.BLOCK_SERVO:
            print("not given valid 'servoType' ")
            return False

        # Check BLOCK_SERVO is valid
        if servoType is DD.BLOCK_SERVO:
            # Check Valid 'servoCoordinate'
            if not (0 <= servoCoordinate) or not (servoCoordinate < self.numBlockCol):
                print("'servoCoordinate' col is out of bounds")
                return False
            if not (servoState is DD.SUBTRACT or servoState is DD.MIDDLE or servoState is DD.ADD):
                print("servoState invalid")
                return False

        # Check LOCK_SERVO is valid    
        if servoType is DD.LOCK_SERVO:
            # Check Valid 'servoCoordinate'
            if not (0 <= servoCoordinate) or not (servoCoordinate < self.numLockRow):
                print("'servoCoordinate' for row is out of bounds")
                return False
            if not (servoState is DD.LOCK or servoState is DD.UNLOCK):
                print("servoState invalid")
                return False

        # Everything is Valid
        return True


if __name__ == '__main__':
    servoJson = 'display_16x16.json'
    dispDimensions = (16, 16) # (width, height)
    servoPm = spm.servo_packet_manager(module_IDs = [10, 14])
    dispInter = display_real_interface(servoJson, dispDimensions, DD.TOP, DD.RIGHT, servoPm) 
    
    while True:
        dispInter.setBlockServos([DD.SUBTRACT] * dispDimensions[0])
        print("SUBTRACT")
        time.sleep(2)

        dispInter.setBlockServos([DD.MIDDLE] * dispDimensions[0])
        print("MIDDLE")
        time.sleep(2)

        dispInter.setLockServos([DD.UNLOCK] * dispDimensions[0])
        print("UNLOCK")
        time.sleep(2)

        dispInter.setBlockServos([DD.ADD] * dispDimensions[0])
        print("ADD")
        time.sleep(2)

        dispInter.setLockServos([DD.LOCK] * dispDimensions[0])
        print("LOCK")
        time.sleep(2)



    