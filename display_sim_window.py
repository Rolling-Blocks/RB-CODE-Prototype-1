import tkinter
from copy import copy, deepcopy

def rgb_cube_func(angle):
    if angle >= 0 and angle < 0.33:
        return 'red'
    if angle >=0.33 and angle < 0.66:
        return 'blue'
    if angle >= 0.66 and angle <= 1.0:
        return 'green'
    return 'white'

def blue_cube_func(angle):
    if angle >= 0 and angle < 0.25:
        return '#8ecae6'
    if angle >=0.25 and angle < 0.5:
        return '#219ebc'
    if angle >= 0.5 and angle < 0.75:
        return '#023047'
    if angle >= 0.75 and angle <= 1.0:
        return '#ffb703'
    return 'white'

def make_array(object, xdim, ydim):
    return [[object for x in range(xdim)] for y in range(ydim)]

class display_window:
    def __init__(self, xcubes, ycubes, cube_x_size, cube_y_size, cube_funcs):
        self.xcubes = xcubes
        self.ycubes = ycubes
        self.cube_x_size = cube_x_size
        self.cube_y_size = cube_y_size
        self.cube_funcs = cube_funcs[:]

        self.root = tkinter.Tk()
        self.root.title('Mechanical Display Simulator')

        xdim = self.cube_x_size * self.xcubes + 100
        ydim = self.cube_y_size * self.ycubes + 100

        self.root.geometry(str(xdim) +'x'+str(ydim))

        self.canvas = tkinter.Canvas(self.root, width=self.cube_x_size * self.xcubes, height=self.cube_y_size * self.ycubes, bg="white")
        self.canvas.pack(pady=50, padx=50)

        for x in range(0,xcubes):
            for y in range(0, ycubes):
                self.set_cube(x,y,0.0)

        self.root.update()
        return
    
    def set_cube(self, x, y, angle):
        filltext = self.cube_funcs[x][y](angle)
        self.canvas.create_rectangle(x*self.cube_x_size, y*self.cube_y_size, (x+1)*self.cube_x_size, (y+1)*self.cube_y_size, fill=filltext)
        return

    def update(self):
        self.root.update()
        return

if __name__ == '__main__':

    window = display_window(10,10,50,50, [[rgb_cube_func for x in range(0,10)] for y in range(0,10)])  

    window.set_cube(0,0,0.5)
    window.update()
    while True:
        i=10