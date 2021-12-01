
class display_sim:
    def __init__(self, sizex, sizey):
        """
            sizex    [int]
            sizey   [int]
                0 1 2 3
                - - - - <--(locks)   x-->
        0    |                      y
        1    |                      |
        2    | <--(rotate servos)  \_/
        3    |
        """
        self.sizex = sizex
        self.sizey = sizey
        self.lock = [0] * sizex
        self.rotate_pos  = [0.0] * sizey
        self.block_angles = [[0.0]*sizey for i in range(sizex)]
    
    def set_locks(self, locks):
        """
            locks   [float[]]
        """
        for x in range(self.sizex):
            if locks[x] > 0.5:
                self.lock[x] = 1
            else:
                self.lock[x] = 0
        
    def set_rotate(self, rotate):
        """
            rotate  [float[]]
        """
        for y in range(self.sizey):
            delta_rotate = rotate[y] - self.rotate_pos[y]
            for x in range(self.sizex):
                if(self.lock[x] == 0):
                    self.block_angles[x][y] += delta_rotate

    def get_angle(self, x, y):
        return self.block_angles[x][y]
    
    def print_display(self, disp_func):
        for y in range(self.sizey):
            line = ""
            for x in range(self.sizex):
                line = line + disp_func(self.block_angles[x][y])
            print(line)

def XO_display(angle):
    if(angle > 0.5):
        return "X"
    return "O"
