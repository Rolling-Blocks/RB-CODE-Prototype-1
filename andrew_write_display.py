from smbus2 import SMBus, i2c_msg
import time

class andrew_write_display:
    def __init__(self, raspi_channel, servo_addresses):
        """
            raspi-channel   [int]
            sevo_addresses  [int[]]
        """
        self.channel = raspi_channel
        self.addresses = servo_addresses
        self.data = []
        self.bus = SMBus(self.channel)
        for addr in servo_addresses:
            self.data.append((addr, [0.0]*16))
    
    def set_servo(self, channel, servo_num, servo_pos):
        """
            channel     [int]
            servo_num   [int]
            servo_pos   [float]
        """
        self.data[channel][1][servo_num] = servo_pos
    
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
    servos = andrew_write_display(1,[10])
    index = 0
    while 1:
        servos.set_servo(0, 11, (index % 255) / 255.0)
        print(index)
        index += 10
        servos.write_servos()
        time.sleep(0.1)