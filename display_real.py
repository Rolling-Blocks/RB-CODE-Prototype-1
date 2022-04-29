import random
import time
from disp_def import DispDef as DD
from disp_def import blockStateKey
import copy
import json
import display_real_interface as dri
import servo_packet_manager as spm
import display

defaultTimesPerMove = {DD.ROWLOCK: 750, DD.COLRETURN: 1000, DD.ROWUNLOCK: 750, DD.COLACTUATE: 1000}

class display_real:
    def __init__(self, display, interface, timePerMove = defaultTimesPerMove):
        
        self.d = display

        # timePerMove is the time buffer corresponding to each time delay
        self.timePerMove = timePerMove

        # Display Real Interface
        self.dispInterface = interface
 
    def setLockServo(self, row, state, updateAfter = True):
        """
            row         [int]
            state       [DD.UNLOCK or DD.LOCK]
            updateAfter [boolean]
        """
        self.d.setBlockServo(col, state)
        if updateAfter:
            self.dispInterface.updateRealDisplay()

    def setLockServos(self, states, updateAfter = True):
        """
            states      [DD.UNLOCK or DD.LOCK]
            updateAfter [boolean]
        """
        #print("setLockServos")
        #print(states)
        self.d.setLockServos(states)
        if updateAfter:
            self.dispInterface.updateRealDisplay()

    def setBlockServo(self, col, state, updateAfter = True):
        """
            col         [int]
            state       [DD.SUBTRACT or DD.MIDDLE or DD.ADD]
            updateAfter [boolean]
        """
        self.d.setBlockServo(col, state)
        if updateAfter:
            self.dispInterface.updateRealDisplay()

    def setBlockServos(self, states, updateAfter = True):    
        """
            state       [DD.SUBTRACT or DD.MIDDLE or DD.ADD]
            updateAfter [boolean]
        """
        self.d.setBlockServos(states)
        if updateAfter:
            self.dispInterface.updateRealDisplay()


    ## sentGcode
        # sentGcode takes in gcode command, 
    def sendGcode(self, arr):
        self.d.sendGcode(arr)

        # Remake and Send Servo Packet
        self.dispInterface.updateRealDisplay()
        
        # Send Back Time Buffer Required To Let Display Finish Move 
        return self.timePerMove[arr[0]]


if __name__ == '__main__':
    disp = display.display((16, 16), DD.TOP, DD.RIGHT, ('#080808','#404040','#B0B0B0','#FFFFFF'), '16x16 display_virtual test')
    servoJson = 'display_16x16.json'
    servoPm = spm.servo_packet_manager(module_IDs = [10, 14])

    dispInter = dri.display_real_interface(disp, servoJson, servoPm) 
    
    timePerMove = {DD.ROWLOCK: 750, DD.COLRETURN: 1000, DD.ROWUNLOCK: 750, DD.COLACTUATE: 1000}
    
    dr = display_real(display = disp, interface = dispInter, timePerMove = timePerMove)

    dispDimensions = disp.getDispDim()

    #disp.printDispVal()

    while True:
        dr.setBlockServos([DD.SUBTRACT] * dispDimensions[0])
        print("SUBTRACT")
        time.sleep(2)

        dr.setBlockServos([DD.MIDDLE] * dispDimensions[0])
        print("MIDDLE")
        time.sleep(2)

        dr.setBlockServos([DD.ADD] * dispDimensions[0])
        print("ADD")
        time.sleep(2)

        dr.setLockServos([DD.LOCK] * dispDimensions[1])
        print("LOCK")
        time.sleep(2)

        dr.setLockServos([DD.UNLOCK] * dispDimensions[1])
        print("UNLOCK")
        time.sleep(2)


    