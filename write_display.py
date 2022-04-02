from smbus2 import SMBus, i2c_msg
import time
#
class write_display:
    def __init__(self, module_IDs = [10, 14], raspi_channel = 1, servoPerModule = 16):
        """
            module_IDs  [int[]]
            raspi-channel   [int] always 1
        """
        self.channel = raspi_channel
        self.module_IDs = module_IDs
        self.bus = SMBus(self.channel)
        self.servoPerModule = servoPerModule
        
        # Generate Servo Dict
        self.servoDict = {}
        for ids in module_IDs:
            self.servoDict[ids] = [0.0 for i in range(servoPerModule)]

    def setServo(self, moduleID, servoID, servo_pos):
        """
            moduleID        [int]
            servoID         [int]
            servo_pos       [float]
        """
        self.servoDict[moduleID][servoID] = servo_pos

    def setServos(self, moduleID, servo_pos):
        """
            channel     [int]
            servo_pos   [float[]]]
        """
        if not len(self.servoPerModule) == len(servo_pos):
            print("setServo in write_display.py given wrong length array")
            return False
        self.servoDict[moduleID][servoID] = servo_pos

    def write_servos(self):
        inBounds = lambda a : int(a * 255) % 256
        for ids in self.module_IDs:
            servoArr = [inBounds(i) for i in self.servoDict[ids]]
            print(servoArr)
            write = i2c_msg.write(ids, servoArr)
            self.bus.i2c_rdwr(write)
    
    def get_servo(self, moduleID, servo_pos):
        return self.servoDict[moduleID][servo_pos]

if __name__ == '__main__':
    servos = write_display()
    servos.setServo(10, 4, 255)
    servos.write_servos()


    index = 0

    while 1:
        for i in range(16):
            servos.setServo(10, i, 255) # 14 locks
        servos.write_servos()
        time.sleep(2)
        for i in range(16):
            servos.setServo(10, i, 1) # 14 locks
        servos.write_servos()
        time.sleep(2)
        