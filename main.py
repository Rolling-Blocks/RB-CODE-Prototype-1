import time
import random
from disp_def import blockStateKey
from disp_def import DispDef as DD
import animation as ani
import image_processor as impr
import display_virtual as disvir
import timer

dispDim = (6, 6) # (width, height)
pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
displayTit = '6x9 test'
a = ani.animation()
ip = impr.image_processor(pixelVal, dispDim)
disp = disvir.display_virtual(displayTit, dispDim, DispDef.TOP, DispDef.RIGHT, pixelVal)  

currentRunningProgram = DD.RUN_RANDIMG
while True:
    # Check Buttons For Changing States
    #check if different State Selected

    if currentRunningProgram is DD.RUN_RANDIMG:
        pass
    if currentRunningProgram is DD.RUN_CLOCK
        pass



