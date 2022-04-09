import tkinter
from disp_def import DispDef as DD
from disp_def import blockStateKey
import time
import display as d

class display_virtual_window:
    def __init__(   self, 
                    display, 
                    blockSideLength = 40, 
                    borderWidth = 10, 
                    servoDim = (30, 8)):
        self.d = display

        self.root = tkinter.Tk()
        self.root.title('Mechanical Display Simulator "' + self.d.getTitle() + '"')

        # state of virtual display stored as cube positions 0-3, position corresponds to color in location in pixelcolors

        self.blockSideLength = blockSideLength
        self.borderWidth = borderWidth
        self.servoDim = servoDim
        
        dispDim = self.d.getDispDim()
        xDispDim = self.servoDim[1] * 2 + dispDim[0] * self.blockSideLength
        yDispDim = self.servoDim[1] * 2 + dispDim[1] * self.blockSideLength

        self.root.geometry(str(xDispDim + self.borderWidth*2) +'x'+str(yDispDim + self.borderWidth*2))

        self.canvas = tkinter.Canvas(self.root, width=xDispDim, height=yDispDim)
        self.canvas.pack(pady=self.borderWidth, padx=self.borderWidth)

        self.updateDisplay()
        return

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

        lockSide =          self.d.getLockBankLocation()
        lockServoState =    self.d.getLockServoState()
        blockSide =         self.d.getBlockBankLocation()
        blockServoState =   self.d.getBlockServoState()
        dispDim =           self.d.getDispDim()
        displayState =      self.d.getDisplayState()
        pixelColors =       self.d.getPixelKey()
        numBlockCol = dispDim[0]
        numLockRow = dispDim[1]

        if lockSide is DD.LEFT:
            # push display down, put servo bars on top
            xBlockOffset += self.servoDim[1] * 2
            # LEFT
            lockServo[0] = self.servoDim[1]/2 
        elif lockSide is DD.RIGHT:
            # RIGHT
            lockServo[0] = self.servoDim[1] * 2 + numBlockCol * self.blockSideLength - self.servoDim[1]*3/2 
        
        if blockSide is DD.TOP:
            # push display down, put servo bars on top
            yBlockOffset += self.servoDim[1] * 2
            # TOP
            blockServo[1] = self.servoDim[1]/2 
        elif blockSide is DD.BOTTOM:
            # BOTTOM
            blockServo[1] = self.servoDim[1] * 2 + numLockRow * self.blockSideLength - self.servoDim[1]*3/2 
        
        blockServo[0] = xBlockOffset + (self.blockSideLength - self.servoDim[0])/2
        lockServo[1] = yBlockOffset + (self.blockSideLength - self.servoDim[0])/2

        for s in range(len(lockServoState)):
            if lockServoState[s] is DD.LOCK:
                f = 'red'
            elif lockServoState[s] is DD.UNLOCK:
                f = 'green'
            else:
                f = 'black'
                print("Black " + str())
            self.canvas.create_rectangle(
                lockServo[0], 
                lockServo[1] + s * self.blockSideLength, 
                lockServo[0] + self.servoDim[1], 
                lockServo[1] + s * self.blockSideLength + self.servoDim[0], 
                fill = f)

        partitionWidth = self.servoDim[0] / 3
        for s in range(0,len(blockServoState)):
            self.canvas.create_rectangle(
                blockServo[0] + s * self.blockSideLength, 
                blockServo[1], 
                blockServo[0] + s * self.blockSideLength + self.servoDim[0], 
                blockServo[1] + self.servoDim[1], 
                fill = 'white')

            offset = partitionWidth *  (1 + blockStateKey(blockServoState[s]))
            self.canvas.create_rectangle(
                blockServo[0] + s * self.blockSideLength + offset, 
                blockServo[1], 
                blockServo[0] + s * self.blockSideLength + offset + partitionWidth, 
                blockServo[1] + self.servoDim[1], 
                fill = 'green')

        
        for y in range(dispDim[1]):
            for x in range(dispDim[0]):
                self.canvas.create_rectangle(
                    xBlockOffset + x * self.blockSideLength, 
                    yBlockOffset + y * self.blockSideLength, 
                    xBlockOffset + (x+1) * self.blockSideLength, 
                    yBlockOffset + (y+1) * self.blockSideLength, 
                    fill = pixelColors[displayState[y][x]])
        self.root.update()

if __name__ == '__main__':
    display = d.display((16, 16), DD.TOP, DD.RIGHT, ('#080808','#404040','#B0B0B0','#FFFFFF'), '16x16 display_virtual_window test')
    window = display_virtual_window(display)  
    i = 1
    while True:
        time.sleep(1)
        window.updateDisplay()
        i += 1
        #print(i)
