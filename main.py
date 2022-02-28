import time
import random
from disp_def import DispDef, blockStateKey
import animation as ani
import image_processor as impr
import display_virtual as disvir
import different_time

dispDim = (6, 6) # (width, height)
pixelVal = ('#CD853F','#8B5A2B','#008080','#D8BFD8')
displayTit = '6x9 test'
a = ani.animation()
ip = impr.image_processor(pixelVal, dispDim)
disp = disvir.display_virtual(displayTit, dispDim, DispDef.TOP, DispDef.RIGHT, pixelVal)  
now = datetime.now()

then = 0
while True:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    time.sleep(1)


#copmiles till here

random.seed(45646481)

servos = write_display.servo_arr(1,[10, 11])
index = 0

lock_all(servos)
for i in range(16):
    servos.set_servo(1,i,0.25)

servos.write_servos()

while True:
    row = random.randrange(4)
    col = random.randrange(4)
    rotate_cube_fwd(servos, row, col)
    row = random.randrange(4)
    col = random.randrange(4)
    rotate_cube_rev(servos, row, col)


