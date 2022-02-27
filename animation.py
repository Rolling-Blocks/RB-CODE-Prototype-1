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

    def _findDifMat(self):
        self.difference = self.desiredState - self.initialState
        self.difference = (self.difference + 1) % 4 - 1
        return self.difference

    def _leastDifRow(self, diffArr):
        difs = self.getDifOfRows(diffArr)
        #print("difs " + str(difs))
        leastIndex = 0
        leastVal = len(difs) * 1000
        for i in range(0,len(difs)):
            if difs[i] < leastVal and not difs[i] == 0:
                leastIndex = i
                leastVal = difs[i]
        #print("least val " + str(difs[leastIndex]))
        return leastIndex

    def _getDifOfRows(self, diffArr):
        rowDifs = np.zeros(len(diffArr))
        for row in range(0,len(diffArr)):
            for col in range(0,len(diffArr[0])): 
                rowDifs[row] += abs(diffArr[row][col])
        return rowDifs

    # Returns what rows the change decreases delta from desired row state.
    def _changeHelpRow(self, diffArr, change):
        changed = copy.deepcopy(diffArr)
        for row in range(0,len(diffArr)):
            for col in range(0,len(diffArr[0])):
                changed[row][col] -= change[col]
        offsetWithChange = self.getDifOfRows(changed)
        #print("offsetWithChange     " + str(offsetWithChange))
        offsetWithoutChange = self.getDifOfRows(diffArr)
        #print("offsetWithoutChange  " + str(offsetWithoutChange)) 

        changeHelp = []
        for row in range(0,len(diffArr)):
            if offsetWithChange[row] < offsetWithoutChange[row]:
                changeHelp.append(row)
        #print("Change Help " + str(changeHelp))
        return changeHelp

    def makeMoveQue(self):
        diffArr = copy.deepcopy(self.findDifMat())
        moveQue = []
        while(True):
            change = copy.deepcopy(diffArr[self.leastDifRow(diffArr)])
            unlock = self.changeHelpRow(diffArr, change) 
            #print("QUE ADDED")
            #print("change: " + str(change))
            #print("unlock: " + str(unlock))
            for i in range(0,len(unlock)): 
                diffArr[unlock[i]] -= change
            diffArr = (diffArr + 1) % 4 -1 
            moveQue.append([change, unlock])
            #time.sleep(.5) 
            if np.all(diffArr == 0):
                break
        #print("diffArr")
        #print(diffArr)     
        return moveQue

    def printMq(self, mq):
        for m in range(0, len(mq)):
            print("Blocks: " + str(mq[m][0]) + " Locks: " + str(mq[m][1]))
                
if __name__ == '__main__':
    w = 16
    h = 16
    a = animation(w, h)

    initState = np.random.randint(0,4, size=(h,w))
    a.setInitialState(initState)
    desState = np.random.randint(0,4, size=(h,w))
    a.setDesiredState(desState)
    diff = a.findDifMat()
    ldRow = a.leastDifRow(diff)

    #print("init")
    #print(initState)
    #print("des")
    #print(desState)
    print("diff")
    print(diff)

    mq = a.makeMoveQue()
    a.printMq(mq)

    i = 1
    while True:
        time.sleep(1)
        i += 1

    