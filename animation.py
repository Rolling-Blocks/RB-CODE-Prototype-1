import skimage
from skimage import color
from skimage import io
import numpy as np
import time
import cv2
import copy
from statistics import mean, stdev

from matplotlib import pyplot as plt
import matplotlib.image as mpimg

class animation:
    def __init__(self, displayWidth = 16, displayHeight = 16):
        # Final Image Dimensions and Colors
        self.dispWidth = displayWidth
        self.dispHeight = displayHeight
        self.initialState = 0
        self.desiredState = 0
        self.difference = 0
        #print(' dimension: ' + str(self.displayWidth) + 'x' + str(self.displayHeight))

    def setInitialState(self, initialState):
        self.initialState = initialState

    def setDesiredState(self, desiredState):
        self.desiredState = desiredState

    def findDif(self):
        self.difference = self.desiredState - self.initialState
        self.difference = (self.difference + 1) % 4 - 1
        return self.difference

if __name__ == '__main__':
    w = 16
    h = 16
    a = animation(w, h)

    initState =  np.random.randint(0,4, size=(h,w))
    print("initialState")
    print(initState)
    a.setInitialState(initState)

    desState =  np.random.randint(0,4, size=(h,w))
    print("desiredState")
    print(desState)
    a.setDesiredState(desState)

    diff = a.findDif()
    print("diff")
    print(diff)

    i = 1
    while True:
        time.sleep(1)
        i += 1

    