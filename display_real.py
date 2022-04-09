import random
import time
from disp_def import DispDef as DD
from disp_def import blockStateKey
import copy
import json
import display_real_interface as dri
import servo_packet_manager as spm
from display import __init__, setLockServo, setBlockServo, setLockServos, setBlockServos, sendGcode

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
        self.dispInterface.setLockServo(row, state, updateAfter)
        self.lockServoState[row] = state

    def setLockServos(self, states, updateAfter = True):
        """
            states      [DD.UNLOCK or DD.LOCK]
            updateAfter [boolean]
        """
        #print("setLockServos")
        #print(states)
        for i in range(len(states)):
            self.dispInterface.setLockServo(i, states[i], False)
            self.lockServoState[i] = states[i]
        if updateAfter:
            self.dispInterface.updateServos()

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

    def setBlockServos(self, states, updateAfter = True):    
        """
            state       [DD.SUBTRACT or DD.MIDDLE or DD.ADD]
            updateAfter [boolean]
        """
        #print("setLockServos")
        #print(states)
        for i in range(len(states)):
            self.dispInterface.setBlockServo(i, states[i], False)
            self.blockServoState[i] = states[i]
        if updateAfter:
            self.dispInterface.updateServos()


    ## sentGcode
        # sentGcode takes in gcode command, 
    def sendGcode(self, arr):
        self.display.sendGcode(arr)

        # Remake and Send Servo Packet
        self.dispInterface.updateRealDisplay()
        
        # Send Back Time Buffer Required To Let Display Finish Move 
        return self.timePerMove[arr[0]]


if __name__ == '__main__':
    display = display.display((16, 16), DD.TOP, DD.RIGHT, ('#080808','#404040','#B0B0B0','#FFFFFF'), '16x16 display_virtual test')
    servoJson = 'display_16x16.json'
    servoPm = spm.servo_packet_manager(module_IDs = [10, 14])

    dispInter = dri.display_real_interface(display, servoJson, servoPm) 
    
    timePerMove = {DD.ROWLOCK: 750, DD.COLRETURN: 1000, DD.ROWUNLOCK: 750, DD.COLACTUATE: 1000}
    
    dr = display_real(display = timePerMove = timePerMove)
    # displayTitle, dispDim, interface, pixelColors, timePerMove  
    
    #disp.printDispVal()

    while True:
        disp.setBlockServos([DD.SUBTRACT] * dispDimensions[0])
        print("SUBTRACT")
        time.sleep(2)

        disp.setBlockServos([DD.MIDDLE] * dispDimensions[0])
        print("MIDDLE")
        time.sleep(2)

        disp.setBlockServos([DD.ADD] * dispDimensions[0])
        print("ADD")
        time.sleep(2)

        disp.setLockServos([DD.LOCK] * dispDimensions[1])
        print("LOCK")
        time.sleep(2)

        disp.setLockServos([DD.UNLOCK] * dispDimensions[1])
        print("UNLOCK")
        time.sleep(2)


    