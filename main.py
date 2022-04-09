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
    print("pi")
    real_Disp = True
else:
    print("not pi")

from disp_def import DispDef    as DD
import numpy                    as np
import animation                as ani
import array_manipulator        as arrMap
import image_processor          as impr
import timer as t
import run_clock as rc
import display

if real_Disp:
    import display_real             as dr
    import display_real_interface   as dri
    import servo_packet_manager     as spm

if not real_Disp:
    import display_virtual          as dv
    import display_virtual_window   as dvw


### Setups Parameters
d = display.display((16, 16), DD.TOP, DD.RIGHT, ('#545454', '#1F1F1F', '#0D0D0D', '#FFFFFF'), '16x16 display_virtual test')

## Times for each move (ROWLOCK, COLRETURN, ROWUNLOCK, COLACTUATE) in ms
timesForMoves = {DD.ROWLOCK: 500, DD.COLRETURN: 500, DD.ROWUNLOCK: 500, DD.COLACTUATE: 500}
a = ani.animation(d.getDispDim())
am = arrMap.array_manipulator()
imgDirectory = "/DispPics"
ip = impr.image_processor(d.getPixelKey(), d.getDispDim(), imgDirectory)

tImage = t.timer()
tClock = t.timer()
tGcode = t.timer()
clockP = rc.run_clock(tClock, d.getDispDim())

if not real_Disp:
    timesForMoves = {DD.ROWLOCK: 100, DD.COLRETURN: 100, DD.ROWUNLOCK: 100, DD.COLACTUATE: 100}
    dispSim = dv.display_virtual(d, timesForMoves)  
else:
    timesForMoves = {DD.ROWLOCK: 250, DD.COLRETURN: 375, DD.ROWUNLOCK: 250, DD.COLACTUATE: 375}
    servoJson = 'display_16x16.json'
    servoPm = spm.servo_packet_manager(module_IDs = [10, 14])
    dispInter = dri.display_real_interface(servoJson, dispDim, blockBank, lockBank, servoPm) 
    dispReal = dr.display_real(displayTitle = displayTit, dispDim = d.getDispDim(), interface = dispInter, pixelColors = d.getPixelKey(), timePerMove = timesForMoves)

# Image Specifiers
imageState = DD.IMG_RAND
imageDefaultPixel = 0
imageLayer = np.full(d.getDispDim(), imageDefaultPixel)

# Clock Specifiers
clockState = DD.CLC_RUN
clockDefaultPixel = 3
clockLayer = np.full(d.getDispDim(), False)

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
        else:
            buffer = dispReal.sendGcode(popped)
        print("Sent Gcode Line, " + str(len(gcode)) + " line left.")

    else:
        ## Stop Image Blank
        if imageState is DD.IMG_NO:
            changed = True
            imageLayer = np.full(d.getDispDim(), imageDefaultPixel)
            imageState = DD.CLC_NULL
            print("IMG_NO")
            
        ## Run Random Image Every Hour
        if imageState is DD.IMG_RAND and (firstTimeRunThrough or tImage.beenHour()):
            firstTimeRunThrough = False
            changed = True
            # Reduces k means clustering values by one if the clock is running
            if clockState is DD.CLC_NO or clockState is DD.CLC_NULL:
                imageLayer = ip.defaultConverter(k = len(d.getPixelKey()))
                print("K means " + str(len(d.getPixelKey())))
            else:
                imageLayer = ip.defaultConverter(k = len(d.getPixelKey()) - 1)
                print("K means " + str(len(d.getPixelKey()) - 1))
            print(imageLayer)
            print("IMG_RAND")

        ## Run One Image
        if imageState is DD.IMG_STATIC:
            changed = True
            # Reduces k means clustering values by one if the clock is running
            if clockState is DD.CLC_NO or clockState is DD.CLC_NULL:
                imageLayer = ip.defaultConverter(k = len(d.getPixelKey()))
            else:
                imageLayer = ip.defaultConverter(k = len(d.getPixelKey()) - 1)
            imageState = DD.CLC_NULL
            print("IMG_STATIC")
        
        ## Stop Clock 
        if clockState is DD.CLC_NO:
            changed = True
            clockLayer = np.full(d.getDispDim(), False)
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
        composite = np.zeros(d.getDispDim())
        # Turn clockLayer from bool to appropriate ints array
        if clockState is DD.CLC_NO or clockState is DD.CLC_NULL:
            print("Just Image Layer")
            composite = imageLayer
        else:
            print("Image and Clock Layer")
            composite = am.incrementArrBy(imageLayer, clockDefaultPixel, len(d.getPixelKey()))
            composite = am.boolMap(composite, clockLayer, clockDefaultPixel)
        
        ## Get Display Current state and composite and get animation and send it to gcode
        a.setInitialState(d.getDisplayState())
        a.setDesiredState(composite)

        print("Making Gcode")
        gcode = a.getGcode()
        print(gcode)
        print("initial")
        print(d.getDisplayState())
        print("final")
        print(composite)

