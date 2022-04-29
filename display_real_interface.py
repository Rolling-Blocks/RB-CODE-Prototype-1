import random
import time
import numpy as np
from disp_def import DispDef as DD
from disp_def import blockStateKey
import copy
import json
import servo_packet_manager as spm
import display as d
# Gets States and handles navigation of JSON and publishing to servos

class display_real_interface:
    def __init__(self, display, servoFile, givenSpm = spm.servo_packet_manager([10,14])):
        """
            display     display
            servoFile   string of Json file title
            givenSpm    servoPacketManager
        """
        with open(servoFile) as json_file:
            self.dispServoData = json.load(json_file)

        self.d = display

        self.servos = givenSpm
        self.updateRealDisplay()

    def writeServos(self):        self.servos.write_servos()
    
    def updateRealDisplay(self):
        self.setLockServos(self.d.getLockServoState())
        self.setBlockServos(self.d.getBlockServoState())
        self.writeServos()

    # Updates Standard Packet To Be Sent
    def __setServo(self, st, sc, state):
        """
            st          DD.LOCK or DD.BLOCK
            sc          int (servocoordinate)
            state       DD. (appropriate)
        """
        # Get Data for Write_Display
        moduleId, servoId, offset = self.__servoInfo(st, sc)
        # Get what ServoPosition would be if no offset and if servoBays in default places 
        defaultServoPos = self.__getPosFromState(servoType = st, servoState = state)
        #print("defaultServoPos givens ~  servoType:" + str(st) + "  servoState:" + str(state))

        toSendToServo = self.__bayCompensator(st, defaultServoPos, offset)
        
        # Sending Data to Write_Display
        self.servos.setServo(moduleId, servoId, toSendToServo)

    # __setServo Helper ~ Json Accessor
        # Given     Servo Type and Coordinate
        # Returns   moduleId, servoId, centerOffset
    def __servoInfo(self, servoType, servoCoordinate): #TODO: Test
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

    # __setServo Helper ~ Turns ServoState To Default Servo Position, does not account for bay position
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

    # __setServo Helper ~ Returns - absolute Servo Set Position
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

        write = self.__bound(0, write, 255)

        if self.d.getLockBankLocation is DD.LEFT or self.d.getBlockBankLocation is DD.BOTTOM:
            write = 255 - write

        return write
    
    def __bound(self, low, high, value): return max(low, min(high, value))
  
    # Write To Singular Row
    def setLockServo(self, row, state, updateAfter = True):
        """
            row         [int]
            state       [DD.LOCK or DD.UNLOCK]
        """
        print("row " + str(row))
        print(state)
        self.__setServo(st = DD.LOCK_SERVO, sc = row, state = state)

        # Update Display
        if updateAfter:
            self.writeServos()

    # Write To Multiple Rows
    def setLockServos(self, states):
        """
            states      [DD.LOCK or DD.UNLOCK]   length same as number of rows
        """
        if not len(states) == self.d.getDispDim()[1]:
            print("setLockServos" + " given invalid number of servo states")
        else:
            for i in range(len(states)):
                self.setLockServo(i, states[i], updateAfter = False)
        self.writeServos()

    ### Copy For Columns once Lock Code Checked    
    def setBlockServo(self, col, state, updateAfter = True):
        """
            col         [int]
            state       DD.SUBTRACT or DD.MIDDLE or DD.ADD
        """
        print("col " + str(col))
        print(state)
        self.__setServo(st = DD.BLOCK_SERVO, sc = col, state = state)

        # Update Display
        if updateAfter:
            self.writeServos()
    
    def setBlockServos(self, states):
        """
            states      [DD.SUBTRACT or DD.MIDDLE or DD.ADD]   length same as number of rows
        """
        if not len(states) == self.d.getDispDim()[0]:
            print("setBlockServos" + " given invalid number of servo states")
        else:
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
    display = d.display((16, 16), DD.TOP, DD.RIGHT, ('#080808','#404040','#B0B0B0','#FFFFFF'), '16x16 display_virtual test')
    servoPm = spm.servo_packet_manager(module_IDs = [10, 14])
    dispInter = display_real_interface(display, servoJson, servoPm) 
    dispDimensions = display.getDispDim()
    
    dispInter.setLockServos([DD.LOCK] * dispDimensions[1])
    print("LOCK")
    time.sleep(.5)

    # dispInter.setLockServos([DD.UNLOCK] * dispDimensions[1])
    # print("UNLOCK")
    # time.sleep(.5)

    dispInter.setBlockServos([DD.MIDDLE] * dispDimensions[1])
    print("LOCK")
    time.sleep(.5)

    dispInter.setLockServos([DD.UNLOCK] * dispDimensions[0])
    print("UNLOCK")
    time.sleep(2)

    dispInter.setBlockServos([DD.ADD] * dispDimensions[0])
    print("ADD")
    time.sleep(2)
    
    if False:
        dispInter.setLockServos([DD.LOCK] * dispDimensions[1])
        print("LOCK")
        time.sleep(.5)

        dispInter.setBlockServos([DD.SUBTRACT] * dispDimensions[0])
        print("SUBTRACT")
        time.sleep(.5)

        dispInter.setLockServos([DD.UNLOCK] * dispDimensions[1])
        print("UNLOCK")
        time.sleep(.5)

        for i in np.arange(0,dispDimensions[0],2):
            print("setBlockServo " + str(i))
            dispInter.setBlockServo(i, DD.MIDDLE, updateAfter = False)
        dispInter.writeServos()
        time.sleep(.75)

        dispInter.setLockServos([DD.LOCK] * dispDimensions[1])
        print("LOCK")
        time.sleep(.5)

        dispInter.setLockServos([DD.UNLOCK] * dispDimensions[1])
        print("UNLOCK")
        time.sleep(.5)

        for i in np.arange(1,dispDimensions[0],2):
            print("setBlockServo " + str(i))
            dispInter.setBlockServo(i, DD.MIDDLE, updateAfter = False)
        dispInter.writeServos()
        time.sleep(.75)

        dispInter.setLockServos([DD.LOCK] * dispDimensions[1])
        print("LOCK")
        time.sleep(.5)

    while False:
        dispInter.setLockServos([DD.LOCK] * dispDimensions[1])
        print("LOCK")y
        time.sleep(.5)

        while True:
            dispInter.setBlockServos([DD.ADD] * dispDimensions[0])
            print("ADD")
            time.sleep(.5)

            dispInter.setBlockServos([DD.SUBTRACT] * dispDimensions[0])
            print("SUBTRACT")
            time.sleep(.5)

    first = True
    while False:

        # dispInter.setBlockServos([DD.MIDDLE] * dispDimensions[0])
        # print("MIDDLE")
        # time.sleep(.375)

        # dispInter.setLockServos([DD.LOCK] * dispDimensions[1])
        # print("LOCK")
        # time.sleep(2)

        dispInter.setLockServos([DD.LOCK] * dispDimensions[1])
        print("LOCK")
        time.sleep(.5)

        dispInter.setLockServos([DD.UNLOCK] * dispDimensions[1])
        print("UNLOCK")
        time.sleep(.5)

        if first:
            first = False

            dispInter.setBlockServos([DD.ADD] * dispDimensions[0])
            print("ADD")
            time.sleep(1)

        # dispInter.setBlockServos([DD.SUBTRACT] * dispDimensions[0])
        # print("SUBTRACT")
        # time.sleep(.375)

        # dispInter.setBlockServos([DD.MIDDLE] * dispDimensions[0])
        # print("MIDDLE")
        # time.sleep(1)

        for i in range(3):
            # Adds
            for i in np.arange(0,dispDimensions[0],2):
                print("setBlockServo " + str(i))
                dispInter.setBlockServo(i, DD.ADD, updateAfter = False)
            dispInter.writeServos()
            time.sleep(.25)

            # middles
            for i in np.arange(0,dispDimensions[0],2):
                print("setBlockServo " + str(i))
                dispInter.setBlockServo(i, DD.SUBTRACT, updateAfter = False)
            dispInter.writeServos()
            time.sleep(.25)


        for i in range(3):
            for i in np.arange(1,dispDimensions[0],2):
                print("setBlockServo " + str(i))
                dispInter.setBlockServo(i, DD.ADD, updateAfter = False)
            dispInter.writeServos()
            time.sleep(.25)


            for i in np.arange(1,dispDimensions[0],2):
                print("setBlockServo " + str(i))
                dispInter.setBlockServo(i, DD.SUBTRACT, updateAfter = False)
            dispInter.writeServos()
            time.sleep(.25)

        dispInter.setLockServos([DD.LOCK] * dispDimensions[1])
        print("LOCK")
        time.sleep(.5)

        dispInter.setLockServos([DD.UNLOCK] * dispDimensions[1])
        print("UNLOCK")
        time.sleep(.5)

        time.sleep(1)
        for i in range(3):
            for i in np.arange(0,dispDimensions[0],2):
                print("setBlockServo " + str(i))
                dispInter.setBlockServo(i, DD.MIDDLE, updateAfter = False)
            dispInter.writeServos()
            time.sleep(.75)


            for i in np.arange(1,dispDimensions[0],2):
                print("setBlockServo " + str(i))
                dispInter.setBlockServo(i, DD.MIDDLE, updateAfter = False)
            dispInter.writeServos()
            time.sleep(.75)
        time.sleep(1)

        dispInter.setLockServos([DD.LOCK] * dispDimensions[0])
        print("LOCK")
        time.sleep(2)



    