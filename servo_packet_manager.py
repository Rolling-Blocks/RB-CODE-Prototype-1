from smbus2 import SMBus, i2c_msg
import time
#
class servo_packet_manager:
    def __init__(self, module_IDs = [10, 14], raspi_channel = 1, servoPerModule = 16):
        """
            module_IDs  [int[]]
            raspi-channel   [int] always 1
        """
        self.module_IDs = module_IDs
        self.bus = SMBus(raspi_channel)
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

    def get_servo(self, moduleID, servo_pos):  
        """
            moduleID        [int]
            servoID         [int]
        """ 
        return self.servoDict[moduleID][servo_pos]
    
    def write_servos(self):
        #print()
        inBounds = lambda a : max(0, min(255, int(a)))
        for ids in self.module_IDs:
            servoArr = [inBounds(i) for i in self.servoDict[ids]]
            #print(str(ids) + " servoArr")
            #print(servoArr)
            write = i2c_msg.write(ids, servoArr)
            self.bus.i2c_rdwr(write)

if __name__ == '__main__':
    servos = servo_packet_manager()
    
    servos.setServo(10, 4, 255)
    servos.write_servos()


    index = 0

    while 1:
        
        for i in range(16):
            servos.setServo(14, i, 128) # 14 locks
        servos.write_servos()
        print("UNLOCK did 128")
        time.sleep(2)
        for i in range(16):
            servos.setServo(14, i, 255) # 14 locks
        servos.write_servos()
        print("LOCK did 255")
        time.sleep(2)
        