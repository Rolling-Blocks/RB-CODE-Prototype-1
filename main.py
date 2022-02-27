import write_display
import time
import random
import DispDef
from animation import __init__, setInitialState, setDesiredState, makeMoveQue
from image_processor import __init__, defaultConverter
import display_virtual
 

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


