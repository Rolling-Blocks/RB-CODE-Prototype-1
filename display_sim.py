import display_sim_window

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
        self.window = display_sim_window.display_window(sizex, sizey,50,50,[[display_sim_window.blue_cube_func for y in range(sizey)] for x in range(sizex)])
        return
    
    def set_locks(self, locks):
        """
            locks   [float[]]
        """
        for x in range(self.sizex):
            if locks[x] > 0.5:
                self.lock[x] = 1
            else:
                self.lock[x] = 0
        return
        
    def set_rotate(self, rotate):
        """
            rotate  [float[]]
        """
        for y in range(self.sizey):
            delta_rotate = rotate[y] - self.rotate_pos[y]
            for x in range(self.sizex):
                if(self.lock[x] == 0):
                    self.block_angles[x][y] += delta_rotate
                    while self.block_angles[x][y] >= 1.0:
                        #self.block_angles[x][y] = 0.99
                        self.block_angles[x][y] -= 1.0
                    while self.block_angles[x][y] <= 0.0:
                        #self.block_angles[x][y] = 0.01
                        self.block_angles[x][y] += 1.0
                    self.window.set_cube(x,y, self.block_angles[x][y])
        return

    def get_angle(self, x, y):
        return self.block_angles[x][y]
    
    def update(self):
        self.window.update()
        return

    '''
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
    '''
if __name__ == '__main__':
    display = display_sim(10,10)
    while True:
        i=10