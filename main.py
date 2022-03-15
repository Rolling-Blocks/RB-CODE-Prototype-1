import time
import random
from disp_def import blockStateKey
from disp_def import DispDef as DD
import numpy as np
import animation as ani
import image_processor as impr
import display_virtual as disvir
import display_virtual_window as dvw
import timer as t
import run_clock as rc

### Setups Parameters
dispDim = (16, 16) # (width, height)
pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
displayTit = '6x9 test'
a = ani.animation()
directory = "\DispPics"
ip = impr.image_processor(pixelVal, dispDim, directory)
tImage = t.timer()
tClock = t.timer()
clockP = rc.run_clock(tClock, dispDim)
#disp = disvir.display_virtual(displayTit, dispDim, DD.TOP, DD.RIGHT, pixelVal)  
dispWind = dvw.display_virtual_window(displayTit, dispDim, DD.TOP, DD.RIGHT, pixelVal)

# Image Specifiers
imageState = DD.IMG_NO
imageDefaultPixel = 0
imageLayer = np.full(dispDim, imageDefaultPixel)

# Clock Specifiers
clockState = DD.CLC_RUN
clockDefaultPixel = 2
clockLayer = np.full(dispDim, False)

# State Manager
changed = False

while True:
    # Check Buttons For Changing States
    
    ## Stop Image Blank
    if imageState is DD.IMG_NO:
        change = True
        imageLayer = np.full(dispDim, 0)
        imageState = DD.CLC_NULL
        
    ## Run Random Image Every Hour
    if imageState is DD.IMG_RAND and tImage.beenHour():
        change = True
        # Reduces k means clustering values by one if the clock is running
        if clockState is DD.CLC_NO:
            imageLayer = ip.defaultConverter(k = len(pixelVal))
        else:
            imageLayer = ip.defaultConverter(k = len(pixelVal) - 1)

    ## Run One Image
    if imageState is DD.IMG_STATIC:
        change = True
        # Reduces k means clustering values by one if the clock is running
        if clockState is DD.CLC_NO:
            imageLayer = ip.defaultConverter(k = len(pixelVal))
        else:
            imageLayer = ip.defaultConverter(k = len(pixelVal) - 1)
        imageState = DD.CLC_NULL
    
    ## Stop Clock 
    if clockState is DD.CLC_NO:
        change = True
        clockLayer = np.full(dispDim, False)

    ## Run Clock
    if clockState is DD.CLC_RUN and tClock.beenMinute():
        change = True
        clockLayer = clockP.getClockArray(lh = 10)
        clockP.printBoolArr(clockLayer)

    if changed == True:
        changed = False
        # Stack Layers
        

