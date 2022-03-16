import time
import random
from disp_def import blockStateKey
from disp_def import DispDef as DD
import numpy as np
import animation as ani
import array_manipulator as arrMap
import image_processor as impr
import display_virtual as disvir
import display_virtual_window as dvw
import timer as t
import run_clock as rc

### Setups Parameters
dispDim = (16, 16) # (width, height)
pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
## Times for each move (ROWLOCK, COLRETURN, ROWUNLOCK, COLACTUATE) in ms
timesForMoves = {DD.ROWLOCK: 500, DD.COLRETURN: 1000, DD.ROWUNLOCK: 500, DD.COLACTUATE: 1000}
displayTit = '6x9 test'
a = ani.animation()
am = arrMap.array_manipulator()
directory = "\DispPics"
ip = impr.image_processor(pixelVal, dispDim, directory)
tImage = t.timer()
tClock = t.timer()
tGcode = t.timer()
clockP = rc.run_clock(tClock, dispDim)
disp = disvir.display_virtual(displayTit, dispDim, DD.TOP, DD.RIGHT, pixelVal, timesForMoves)  
#dispWind = dvw.display_virtual_window(displayTit, dispDim, DD.TOP, DD.RIGHT, pixelVal)

# Image Specifiers
imageState = DD.IMG_NO
imageDefaultPixel = 0
imageLayer = np.full(dispDim, imageDefaultPixel)

# Clock Specifiers
clockState = DD.CLC_RUN
clockDefaultPixel = 2
clockLayer = np.full(dispDim, False)

# Gcode
gcode = []
buffer = 500

# State Manager
changed = False

while True:
    # Check Buttons For Changing States
    
    if not len(gcode) == 0 and tGcode.beenXmils(buffer):
        popped = gcode.pop(0)
        buffer = disp.sendGcode(popped)
        print("Sent Gcode Line, " + str(len(gcode)) + " line left.")

    else:
        ## Stop Image Blank
        if imageState is DD.IMG_NO:
            changed = True
            imageLayer = np.full(dispDim, imageDefaultPixel)
            imageState = DD.CLC_NULL
            print("IMG_NO")
            
        ## Run Random Image Every Hour
        if imageState is DD.IMG_RAND and tImage.beenHour():
            changed = True
            # Reduces k means clustering values by one if the clock is running
            if clockState is DD.CLC_NO:
                imageLayer = ip.defaultConverter(k = len(pixelVal))
            else:
                imageLayer = ip.defaultConverter(k = len(pixelVal) - 1)
            print("IMG_RAND")

        ## Run One Image
        if imageState is DD.IMG_STATIC:
            changed = True
            # Reduces k means clustering values by one if the clock is running
            if clockState is DD.CLC_NO:
                imageLayer = ip.defaultConverter(k = len(pixelVal))
            else:
                imageLayer = ip.defaultConverter(k = len(pixelVal) - 1)
            imageState = DD.CLC_NULL
            print("IMG_STATIC")
        
        ## Stop Clock 
        if clockState is DD.CLC_NO:
            changed = True
            clockLayer = np.full(dispDim, False)
            print("CLC_NO")

        ## Run Clock
        if clockState is DD.CLC_RUN and tClock.beenMinute():
            changed = True
            clockLayer = clockP.getClockArray(lh = 10)
            clockP.printBoolArr(clockLayer)
            print("CLC_RUN")

    ## Display has changed and gcode needs to be made
    if changed == True and len(gcode) == 0:
        changed = False
        # Stack Layers
        composite = np.zeros(dispDim)
        # Turn clockLayer from bool to appropriate ints array
        if clockState is DD.CLC_NO:
            print("Just Image Layer")
            composite = imageLayer
        else:
            print("Image and Clock Layer")
            composite = am.incrementArrBy(imageLayer, clockDefaultPixel, len(pixelVal))
            composite = am.boolMap(composite, clockLayer, clockDefaultPixel)
        ## Get Display Current state and composite and get animation and send it to gcode
        a.setInitialState(disp.getDisplayState())
        a.setDesiredState(composite)
        print("Making Gcode")
        gcode = a.getGcode()
        print(gcode)

