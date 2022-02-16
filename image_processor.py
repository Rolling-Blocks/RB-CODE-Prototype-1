import skimage
from skimage import color
from skimage import io
import numpy as numpy
import cv2

from matplotlib import pyplot as plt
import matplotlib.image as mpimg

class image_processor:
    def __init__(self, pixelValues, displayWidth = 16, displayHeight = 16, displayName = 'generic display'):
        # Final Image Dimensions and Colors
        self.dispWidth = displayWidth
        self.dispHeight = displayHeight
        self.pixelColors = pixelValues

        print('processor extablished for ' + displayName + ' dimension: ' + str(self.displayWidth) + 'x' + str(self.displayHeight) + ' pixel values: ' + pixelValues)

if __name__ == '__main__':
    img = cv2.imread('Ideas_Surprised_Pikachu_HD.jpg')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    resized = cv2.resize(img, (16,16), interpolation = cv2.INTER_AREA)

    resized[9][12] = 0
    resized[12][9] = 0


    plt.imshow(imgGray, cmap='gray')

    plt.show()