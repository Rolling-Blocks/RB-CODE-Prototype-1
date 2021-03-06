import numpy as np
import time, cv2, copy, os, random, sys

# Check if Running On Pi

import io 
import os

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

from matplotlib import pyplot as plt
import matplotlib.image as mpimg

class image_processor:
    def __init__(self, pixelValues, displayDim, image_folder): #displayName = 'generic display'
        # Final Image Dimensions and Colors
        self.dispWidth = displayDim[0]
        self.dispHeight = displayDim[1]
        self.pixelColors = pixelValues

        self.image_folder = image_folder

        #print('processor extablished for ' + displayName + ' dimension: ' + str(self.displayWidth) + 'x' + str(self.displayHeight) + ' pixel values: ' + pixelValues)

    def newImage(self, image_title):
        self.imgTitle = str(sys.path[0])+ '\DispPics' + str(image_title)
        print("imported Image Title = " + self.imgTitle + " ----- of type " + str(type(self.imgTitle)))

    def getImageTitle(self):
        return self.imgTitle

    def __displayRGB(self):
        r = self.__imageResizeRGB()
        plt.imshow(r)
        plt.show()

    # split self off
    def __imageResizeRGB(self):
        img = cv2.imread(self.imgTitle)
        resized = cv2.resize(img, (self.dispWidth, self.dispHeight), interpolation = cv2.INTER_AREA)
        return resized

    def __displayBW(self):
        r = self._imageResizeBW()
        plt.imshow(r, cmap = "gray")
        plt.show()

    # split self off
    def __imageResizeBW(self):
        img = cv2.imread(self.imgTitle)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(imgGray, (self.dispWidth, self.dispHeight), interpolation = cv2.INTER_AREA)
        return resized

    def __reduceColors(self, img, K):
        n = img[0][0].size
        Z = img.reshape((-1,n))

        # convert to np.float32
        Z = np.float32(Z)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((img.shape))
        return res2

    def __removeColors(self, img):
        recorded = np.unique(img)
        imgCopy = copy.deepcopy(img)
        for y in range(0,len(img)):        
            for x in range(0,len(img[0])):
                for n in range(0,len(recorded)):
                    if imgCopy[y][x] == recorded[n]:
                        imgCopy[y][x] = n
        return imgCopy

    def defaultConverter(self, imgTit = False, k = 4):
        if imgTit is False:
            self.getRandomImage()
        else:
            self.newImage(imgTit)
        bw = self.__imageResizeBW()
        lowRes = self.__reduceColors(bw, k)
        remapped = self.__removeColors(lowRes)
        return remapped

    # Fucking Hell getRandomImage not working consistently
    def getRandomImage(self):
        #Compensate if is real raspberry pi

        n=0
        random.seed()
        print("penis")
        print(str(sys.path[0]) + self.image_folder)
        print("penis")

        for root, dirs, files in os.walk(str(sys.path[0]) + self.image_folder):
            print("penis")
            for name in files:
                n += 1
                if random.uniform(0, n) < 1:
                    print("got rfile")
                    rfile = os.path.join(root, name)
                else:
                    print("rfile not selected")
        print(rfile)
        self.imgTitle = rfile

if __name__ == '__main__':
    dispDim = (16, 16)
    directory = "/DispPics"
    ip = image_processor(('#CD853F','#8B5A2B','#008080','#D8BFD8'), dispDim, directory)
    print(ip.defaultConverter(k = 3))
    i = 1
    while True:
        time.sleep(1)
        i += 1

    