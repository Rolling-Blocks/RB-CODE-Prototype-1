from smbus2 import SMBus, i2c_msg
import time
#
class write_display:
    def __init__(self, raspi_channel = 1, servo_addresses = [10, 14]):
        """
            raspi-channel   [int] always 1
            sevo_addresses  [int[]]
        """
        self.channel = raspi_channel
        self.addresses = servo_addresses
        self.data = []
        self.bus = SMBus(self.channel)
        for addr in servo_addresses:
            self.data.append((addr, [0.0]*16))

    def set_servo(self, moduleID, servoModuleID, servo_pos):
        """
            moduleID        [int]
            servoModuleID   [int]
            servo_pos       [float]
        """
        self.data[moduleID][1][servoModuleID] = servo_pos
    
    def set_servo_arr(self, channel, servo_pos):
        """
            channel     [int]
            servo_pos   [float[]]]
        """
        for i in range(16):
            self.data[channel][1][i] = servo_pos[i]

    def write_servos(self):
        for tup in self.data:
            write = i2c_msg.write(tup[0], [(int(i * 255) % 256) for i in tup[1]])
            self.bus.i2c_rdwr(write)
    
    def get_servo(self, channel, servo_pos):
        return self.data[channel][1][servo_pos]

if __name__ == '__main__':
    servos = write_display()
    index = 0

    while 1:
        for i in range(16):
            servos.set_servo(1, i, (index % 255) / 255.0) # 14 locks
        print(index)
        index += 10
        servos.write_servos()
        time.sleep(0.04)
        