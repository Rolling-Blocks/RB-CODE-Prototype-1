# Checkboard BackDrop
# Shows Time in Hours and Minutes Like Classic Analog Clock

import time
import random
from disp_def import DispDef, blockStateKey
import animation as ani
import image_processor as impr
import display_virtual as disvir
import timer as tim
import numpy as np

class run_clock:
    def __init__(self, t, a):
        self.timmo = t
        self.animator = a

    def getClockGcode(self, blankBackground):
        currentTime = self.timmo.getThen()
        print(currentTime)

    def printNumber(self, w, h, number):
        num = self.__makeNumber(w, h, number)
        print(number)
        self.__printBoolArr(num)

    def __makeNumber(self, w, h, number):
        numArray = np.full((h, w), False)
        linesToFill = self.__getSegments(number)
        #print(number)
        #print(linesToFill)
        for index in range(0, len(linesToFill)):
            #print("Segment Array")
            segmentNum = linesToFill[index]
            sd = self.__numToSegment(w, h, segmentNum)
            segmentArr = self.__fillLine(w, h, sd[1], sd[0])
            #print(segmentArr)
            numArray = np.logical_or(numArray, segmentArr)
            #print()
        
        # Added Features To Font
        if (h >= 6) and (h%2 == 0) and (number == 3):
            numArray[h-2][0] = True
        if (h >= 6) and (h%2 == 0) and (number == 2):
            numArray[h-2][w-1] = True
        if (h >= 6) and (h%2 == 0) and (number == 5):
            numArray[h-2][0] = True
        if (h >= 5) and (number == 7):
            numArray[1][0] = True
        return numArray
            
    # Number to Segments To Fill        
    def __getSegments(self, num):
        numMap = {
            -1: (),
            0: (0, 1, 2, 4, 5, 6),
            1: (2, 5),
            2: (0, 2, 3, 4, 6),
            3: (0, 2, 3, 5, 6),
            4: (1, 2, 3, 5),
            5: (0, 1, 3, 5, 6),
            6: (0, 1, 3, 4, 5, 6),
            7: (0, 2, 5),
            8: (0, 1, 2, 3, 4, 5, 6),
            9: (0, 1, 2, 3, 5)
        }
        return numMap[num]

    # Segment to Dimension Fill 
    def __numToSegment(self, w, h, segmentNum):
        # Mid Line Height
        ml = int((h + (h % 2))/2 - 1)
        segmentKey = {
            # (height, width)
            0: ((0, 0),     (0, w-1)    ),
            1: ((0, ml),    (0, 0)      ),
            2: ((0, ml),    (w-1, w-1)  ),
            3: ((ml, ml),   (0, w-1)    ),
            4: ((ml, h-1),  (0, 0)      ),
            5: ((ml, h-1),  (w-1, w-1)  ),
            6: ((h-1, h-1), (0, w-1)    )
        }
        return segmentKey[segmentNum]

    # Fill Line
        # Returns Array of Digit Dimension Full of Falses with Trues where the line is. 
        # dh ~ digit height
        # dw ~ digit width
        # lh ~ line height  (bottom, top)
        # lw ~ line width   (left, right)
    def __fillLine(self, dh, dw, lh, lw):
        numArray = np.full((dw, dh), False)
        #print("Line Dimensions " + str(lh) + " : " + str(lw))
        for y in range(lh[0], lh[1] + 1):
            for x in range(lw[0], lw[1] + 1):
                #print("(x " + str(x) + ", y " + str(y) + ")")
                numArray[x][y] = True
        return numArray

    # Print 2d Boolean Array as 1s and 0s
    def __printBoolArr(self, arr):
        numArray = np.full((h, w), 0)
        for x in range(0, w):
            for y in range(0, h):
                if arr[y][x]:
                    numArray[y][x] = 1
        print(numArray)
        print()

if __name__ == '__main__':
    tim = tim.timer()
    ani = ani.animation(16, 16)
    rc = run_clock(tim, ani)

    w = 3
    h = 8
    
    for i in range(-1, 10):
        rc.printNumber(w, h, i)