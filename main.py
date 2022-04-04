# Check if Running On Pi

import io 
import os

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

real_Disp = 0
if is_raspberrypi():
    print("Linux")
    real_Disp = True
else:
    print("win32")

from disp_def import DispDef    as DD
import numpy                    as np
import animation                as ani
import array_manipulator        as arrMap
import image_processor          as impr
import timer as t
import run_clock as rc

if real_Disp:
    import display_real             as dr
    import display_real_interface   as dri
if not real_Disp:
    import display_virtual          as dv
    import display_virtual_window   as dvw


### Setups Parameters
dispDim = (16, 16) # (width, height)
pixelVal = ('#E1523D','#ED8B16','#C2BB00','#003547')
pixelVal = ('#545454', '#1F1F1F', '#0D0D0D', '#FFFFFF')
## Times for each move (ROWLOCK, COLRETURN, ROWUNLOCK, COLACTUATE) in ms
timesForMoves = {DD.ROWLOCK: 200, DD.COLRETURN: 200, DD.ROWUNLOCK: 200, DD.COLACTUATE: 200}
displayTit = '6x9 test'
a = ani.animation(dispDim)
am = arrMap.array_manipulator()
directory = "\DispPics"
ip = impr.image_processor(pixelVal, dispDim, directory)
tImage = t.timer()
tClock = t.timer()
tGcode = t.timer()
clockP = rc.run_clock(tClock, dispDim)
if not real_Disp:
    dispSim = dv.display_virtual(displayTit, dispDim, DD.TOP, DD.RIGHT, pixelVal, timesForMoves)  
    #dispWind = dvw.display_virtual_window(displayTit, dispDim, DD.TOP, DD.RIGHT, pixelVal)

# Image Specifiers
imageState = DD.IMG_RAND
imageDefaultPixel = 0
imageLayer = np.full(dispDim, imageDefaultPixel)

# Clock Specifiers
clockState = DD.CLC_RUN
clockDefaultPixel = 3
clockLayer = np.full(dispDim, False)

# Gcode
gcode = []
buffer = 500

# State Manager
changed = False

firstTimeRunThrough = True

while True:
    # Check Buttons For Changing States
    if not len(gcode) == 0 and tGcode.beenXmils(buffer):
        popped = gcode.pop(0)
        if not real_Disp:
            buffer = dispSim.sendGcode(popped)
        print("Sent Gcode Line, " + str(len(gcode)) + " line left.")

    else:
        ## Stop Image Blank
        if imageState is DD.IMG_NO:
            changed = True
            imageLayer = np.full(dispDim, imageDefaultPixel)
            imageState = DD.CLC_NULL
            print("IMG_NO")
            
        ## Run Random Image Every Hour
        if imageState is DD.IMG_RAND and (firstTimeRunThrough or tImage.beenHour()):
            firstTimeRunThrough = False
            changed = True
            # Reduces k means clustering values by one if the clock is running
            if clockState is DD.CLC_NO or clockState is DD.CLC_NULL:
                imageLayer = ip.defaultConverter(k = len(pixelVal))
                print("K means " + str(len(pixelVal)))
            else:
                imageLayer = ip.defaultConverter(k = len(pixelVal) - 1)
                print("K means " + str(len(pixelVal) - 1))
            print(imageLayer)
            print("IMG_RAND")

        ## Run One Image
        if imageState is DD.IMG_STATIC:
            changed = True
            # Reduces k means clustering values by one if the clock is running
            if clockState is DD.CLC_NO or clockState is DD.CLC_NULL:
                imageLayer = ip.defaultConverter(k = len(pixelVal))
            else:
                imageLayer = ip.defaultConverter(k = len(pixelVal) - 1)
            imageState = DD.CLC_NULL
            print("IMG_STATIC")
        
        ## Stop Clock 
        if clockState is DD.CLC_NO:
            changed = True
            clockLayer = np.full(dispDim, False)
            clockState = DD.CLC_NULL
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
        if clockState is DD.CLC_NO or clockState is DD.CLC_NULL:
            print("Just Image Layer")
            composite = imageLayer
        else:
            print("Image and Clock Layer")
            composite = am.incrementArrBy(imageLayer, clockDefaultPixel, len(pixelVal))
            composite = am.boolMap(composite, clockLayer, clockDefaultPixel)
        ## Get Display Current state and composite and get animation and send it to gcode
        a.setInitialState(dispSim.getDisplayState())
        a.setDesiredState(composite)
        print("Making Gcode")
        gcode = a.getGcode()
        print(gcode)

