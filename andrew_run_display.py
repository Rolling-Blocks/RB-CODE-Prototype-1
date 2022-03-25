import andrew_write_display as write_display
import time
import random

def lock_all(servodisp):
    for i in range(16):
        servodisp.set_servo(0,i,0.0)
    servodisp.write_servos()
    time.sleep(0.3)

def unlock_row(servodisp, col):
    servodisp.set_servo(0,col,1.0)
    servodisp.write_servos()
    time.sleep(0.3)

def unlock_all(servodisp):
    for i in range(16):
        servodisp.set_servo(0,i,1.0)
    servodisp.write_servos()
    time.sleep(0.3)

def smooth_rotate(servodisp, row, position):
    init_pos = servodisp.get_servo(1,row)
    delta = (position - init_pos) / 40
    adjacent_delta = 0.05
    if delta < 0:
        adjacent_delta *= -1.0

    if row - 1 >= 0:
        servodisp.set_servo(1, row - 1, servodisp.get_servo(1,row - 1) + adjacent_delta)
    if row + 1 <= 15:
        servodisp.set_servo(1, row + 1, servodisp.get_servo(1,row + 1) + adjacent_delta)
    servodisp.write_servos()
    time.sleep(0.5)
    for i in range(20):
        servodisp.set_servo(1, row, init_pos + delta * (i + 1))
        servodisp.write_servos()
        time.sleep(0.02)
    
    adjacent_delta *= -1.0
    if row - 1 >= 0:
        servodisp.set_servo(1, row - 1, servodisp.get_servo(1,row - 1) + 2 * adjacent_delta)
    if row + 1 <= 15:
        servodisp.set_servo(1, row + 1, servodisp.get_servo(1,row + 1) + 2 * adjacent_delta)
    servodisp.write_servos()
    time.sleep(0.3)
    for i in range(20):
        servodisp.set_servo(1, row, init_pos + delta * (i + 21))
        servodisp.write_servos()
        time.sleep(0.02)
    adjacent_delta *= -1.0
    if row - 1 >= 0:
        servodisp.set_servo(1, row - 1, servodisp.get_servo(1,row - 1) + adjacent_delta)
    if row + 1 <= 15:
        servodisp.set_servo(1, row + 1, servodisp.get_servo(1,row + 1) + adjacent_delta)

def set_locks(position, servodisp):
    for i in range(4):
            servodisp.set_servo(0,i,position)

def rotate_cube_fwd(servodisp, row, col):
    servos = servodisp
    lock_all(servos)
    servos.set_servo(1,col,0.2)
    servos.write_servos()
    time.sleep(0.5)
    unlock_row(servos, row)
    smooth_rotate(servos, col, 0.9)
    lock_all(servos)

def rotate_cube_rev(servodisp, row, col):
    servos = servodisp
    lock_all(servos)
    servos.set_servo(1,col,0.9)
    servos.write_servos()
    time.sleep(0.5)
    unlock_row(servos, row)
    smooth_rotate(servos, col, 0.2)
    lock_all(servos)

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


