import write_display
import display_sim
import time


servos = write_display.servo_arr(1,[10])
index = 0
while 1:
    #servos.set_servo(0, 11, index / 255.0)
    #index += 10
    servos.set_servo(0, 1, 1.0)
    servos.set_servo(0, 2, 1.0)
    servos.set_servo(0, 3, 1.0)
    servos.set_servo(0, 4, 1.0)
    servos.set_servo(0, 5, 1.0)
    servos.set_servo(0, 6, 1.0)
    servos.write_servos()
    time.sleep(2)
    servos.set_servo(0, 1, 0.0)
    servos.set_servo(0, 2, 0.0)
    servos.set_servo(0, 3, 0.0)
    servos.set_servo(0, 4, 0.0)
    servos.set_servo(0, 5, 0.0)
    servos.set_servo(0, 6, 0.0)
    servos.write_servos()
    time.sleep(2)