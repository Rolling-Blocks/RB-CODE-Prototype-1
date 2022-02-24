import skimage
from skimage import color
from skimage import io
import numpy as np
import time
import cv2
from statistics import mean, stdev

from matplotlib import pyplot as plt
import matplotlib.image as mpimg

class image_processor:
    def __init__(self, pixelValues, displayWidth = 16, displayHeight = 16): #displayName = 'generic display'
        # Final Image Dimensions and Colors
        self.dispWidth = displayWidth
        self.dispHeight = displayHeight
        self.pixelColors = pixelValues

        #print('processor extablished for ' + displayName + ' dimension: ' + str(self.displayWidth) + 'x' + str(self.displayHeight) + ' pixel values: ' + pixelValues)

    def newImage(self, image_title):
        self.imgTitle = image_title
        print("imported Image Title = " + self.imgTitle + " ----- of type " + str(type(self.imgTitle)))

    def pixelAverageVal(self, downsized):
        sum = 0
        print(downsized.shape)
        h, w = downsized.shape
        for y in range(0,h):
            for x in range(0,w):
                sum += downsized[y][x]
        return sum / (h * w)

    def displayRGB(self):
        r = self.imageResizeRGB()
        plt.imshow(r)
        plt.show()

    def imageResizeRGB(self):
        img = cv2.imread(self.imgTitle)
        resized = cv2.resize(img, (self.dispWidth, self.dispHeight), interpolation = cv2.INTER_AREA)
        return resized

    def displayBW(self):
        r = self.imageResizeBW()
        plt.imshow(r, cmap = "gray")
        plt.show()

    def imageResizeBW(self):
        img = cv2.imread(self.imgTitle)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(imgGray, (self.dispWidth, self.dispHeight), interpolation = cv2.INTER_AREA)
        return resized

if __name__ == '__main__':
    ip = image_processor(('#CD853F','#8B5A2B','#008080','#D8BFD8'), 16, 16)
    ip.newImage('Ideas_Surprised_Pikachu_HD.jpg')
    ip.displayRGB()

    i = 0
    while True:
        time.sleep(1)
        i += 1