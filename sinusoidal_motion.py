import display_sim
import random
import math
import time

from display_sim_window import display_window

xsize = 16
ysize = 16

display = display_sim.display_sim(xsize,ysize)
random.seed(11337+455456)
lockinfo = []
for x in range(xsize):
    lockinfo.append((random.randint(10,100), random.randint(10,100)))

motioninfo = []
for y in range(ysize):
    motioninfo.append((random.randint(60,100), random.randint(60,100)))

iteration = 0.0

while True:
    lockarr = []
    for lock in lockinfo:
        lockarr.append(random.randint(3,10)/10)
    motionarr = []
    for motion in motioninfo:
        motionarr.append(math.sin(motion[0]*(motion[1]+iteration)/100)/5)
    display.set_locks(lockarr)
    display.set_rotate(motionarr)
    display.update()
    #print(motionarr)
    #print(lockarr)
    iteration += 0.02
    time.sleep(2)