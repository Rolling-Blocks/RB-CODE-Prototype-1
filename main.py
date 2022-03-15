import time
import random
from disp_def import blockStateKey
from disp_def import DispDef as DD
import numpy as np
import animation as ani
import image_processor as impr
import display_virtual as disvir
import display_virtual_window as dvw
import timer
import run_clock as rc

### Setups Parameters
dispDim = (16, 16) # (width, height)
pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
displayTit = '6x9 test'
a = ani.animation()
directory = "\DispPics"
ip = impr.image_processor(pixelVal, dispDim, directory)
tClock = timer.timer()
clockP = rc.run_clock(tClock, dispDim)
#disp = disvir.display_virtual(displayTit, dispDim, DD.TOP, DD.RIGHT, pixelVal)  
dispWind = dvw.display_virtual_window(displayTit, dispDim, DD.TOP, DD.RIGHT, pixelVal)

# Image Specifiers
imageDefaultPixel = 0
imageLayer = np.full(dispDim, imageDefaultPixel)
imageShutOff = True

# Clock Specifiers
clockDefaultPixel = 2
clockLayer = np.full(dispDim, False)
clockShutOff = False

currentRunningProgram = DD.RUN_CLOCK
while True:
    # Check Buttons For Changing States
    #check if different State Selected
    if currentRunningProgram is DD.RUN_RANDIMG:
        pass
    
    ## Run Clock
    if currentRunningProgram is DD.RUN_CLOCK:
        clockCleared = False
        if tClock.beenMinute():
            clockLayer = clockP.getClockArray(lh = 10)
            clockP.printBoolArr(clockLayer)
    else:
        # set clock layer to blank
        if clockCleared == False:
            clockCleared = True
            clockLayer = np.full(DispDef, False)