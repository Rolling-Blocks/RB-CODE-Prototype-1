import tkinter
from disp_def import DispDef, blockStateKey
import time
from PIL import ImageColor
from copy import copy, deepcopy

class display_virtual_window:
    def __init__(   self, 
                    displayTitle, 
                    dismDim, 
                    blockSide, 
                    lockSide, 
                    pixelColors, 
                    blockSideLength = 40, 
                    borderWidth = 30, 
                    servoDim = (30, 12)):
        # numLockRow ~ Height of Diplay
        self.numLockRow = dismDim[1]
        # lockSide ~ left/right
        self.lockSide = lockSide
        # numBlockCol ~ width of Diplay
        self.numBlockCol = dismDim[0]
        # blockSide ~ top/bottom
        self.blockSide = blockSide
        # pixelColors (pixelcolor0,pixelcolor1,pixelcolor2,pixelcolor3) pixel color values  
        self.pixelColors = pixelColors

        self.root = tkinter.Tk()
        self.root.title('Mechanical Display Simulator "' + displayTitle + '"')

        # state of virtual display stored as cube positions 0-3, position corresponds to color in location in pixelcolors
        self.displayState = [[0]*self.numBlockCol for i in range(self.numLockRow)]
        
        #states of locks unlocked/locked
        self.lockServoState = [DispDef.UNLOCK]*self.numLockRow

        # display viewer setup
        self.blockServoState = [DispDef.MIDDLE]*self.numBlockCol

        self.blockSideLength = blockSideLength
        self.borderWidth = borderWidth
        self.servoDim = servoDim
        xDispDim = self.servoDim[1] * 2 + self.numBlockCol * self.blockSideLength
        yDispDim = self.servoDim[1] * 2 + self.numLockRow * self.blockSideLength

        self.root.geometry(str(xDispDim + self.borderWidth*2) +'x'+str(yDispDim + self.borderWidth*2))

        self.canvas = tkinter.Canvas(self.root, width=xDispDim, height=yDispDim)
        self.canvas.pack(pady=self.borderWidth, padx=self.borderWidth)

        self.updateDisplay()
        return

    def setFrameLocks(self, displayState, lockState, blockStates):
        self.displayState = displayState
        self.lockServoState = lockState
        self.blockServoState = blockStates
        self.updateDisplay()

    def setFrame(self, displayState):
        self.displayState = displayState
        self.updateDisplay()

    def setLocks(self, lockState, blockStates):
        self.lockServoState = lockState
        self.blockServoState = blockStates
        self.updateDisplay()

    # Makes Display Image
        # Draws Actuator Positions
        # Draws Block Positions
    def updateDisplay(self):
        self.canvas.delete("all")
        
        xBlockOffset = 5
        yBlockOffset = -5

        # Top Left of Servo Bars
        lockServo = [0, 0]
        blockServo = [0, 0]

        if self.lockSide is DispDef.LEFT:
            # push display down, put servo bars on top
            xBlockOffset += self.servoDim[1] * 2
            # LEFT
            lockServo[0] = self.servoDim[1]/2 

        if self.lockSide is DispDef.RIGHT:
            # RIGHT
            lockServo[0] = self.servoDim[1] * 2 + self.numBlockCol * self.blockSideLength - self.servoDim[1]*3/2 
        
        if self.blockSide is DispDef.TOP:
            # push display down, put servo bars on top
            yBlockOffset += self.servoDim[1] * 2
            # TOP
            blockServo[1] = self.servoDim[1]/2 
        
        if self.blockSide is DispDef.BOTTOM:
            # BOTTOM
            blockServo[1] = self.servoDim[1] * 2 + self.numLockRow * self.blockSideLength - self.servoDim[1]*3/2 
        
        blockServo[0] = xBlockOffset + (self.blockSideLength - self.servoDim[0])/2
        lockServo[1] = yBlockOffset + (self.blockSideLength - self.servoDim[0])/2

        for s in range(0,len(self.lockServoState)):
            if self.lockServoState[s] is DispDef.LOCK:
                f = 'red'
            if self.lockServoState[s] is DispDef.UNLOCK:
                f = 'green'
            self.canvas.create_rectangle(
                lockServo[0], 
                lockServo[1] + s * self.blockSideLength, 
                lockServo[0] + self.servoDim[1], 
                lockServo[1] + s * self.blockSideLength + self.servoDim[0], 
                fill = f)

        partitionWidth = self.servoDim[0] / 3
        for s in range(0,len(self.blockServoState)):
            self.canvas.create_rectangle(
                blockServo[0] + s * self.blockSideLength, 
                blockServo[1], 
                blockServo[0] + s * self.blockSideLength + self.servoDim[0], 
                blockServo[1] + self.servoDim[1], 
                fill = 'white')

            offset = partitionWidth *  (1 + blockStateKey(self.blockServoState[s]))
            self.canvas.create_rectangle(
                blockServo[0] + s * self.blockSideLength + offset, 
                blockServo[1], 
                blockServo[0] + s * self.blockSideLength + offset + partitionWidth, 
                blockServo[1] + self.servoDim[1], 
                fill = 'green')

        for y in range(0,self.numLockRow):
            for x in range(0,self.numBlockCol):
                self.canvas.create_rectangle(
                    xBlockOffset + x * self.blockSideLength, 
                    yBlockOffset + y * self.blockSideLength, 
                    xBlockOffset + (x+1) * self.blockSideLength, 
                    yBlockOffset + (y+1) * self.blockSideLength, 
                    fill = self.pixelColors[self.displayState[y][x]])
        self.root.update()
        return

if __name__ == '__main__':
    dispDim = (5, 9) # (width, height)
    pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
    displayTit = '6x9 test'
    window = display_virtual_window(displayTit, 
                                    dispDim, 
                                    DispDef.TOP, 
                                    DispDef.RIGHT, 
                                    pixelVal)  
    i = 1
    while True:
        time.sleep(1)
        window.updateDisplay()
        i += 1
        #print(i)
