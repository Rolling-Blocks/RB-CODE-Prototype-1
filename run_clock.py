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
import copy

class run_clock:
    def __init__(self, t, a):
        self.timmo = t
        self.animator = a

    def getClockGcode(self, blankBackground):
        currentTime = self.timmo.getThen()
        print(currentTime)

    def printDigit(self, w, h, number):
        num = self.__makeNumber(w, h, number)
        self.printBoolArr(num)
    
    def __combineMatrices(self, one, two):
        onetwo = [[0] * (len(one[0]) + len(two[0])) for i in range(len(one))]
        #print("onetwo: ")
        #print("")
        for y in range(len(one)):
            a = 0
            for i in range(len(one[0])):
                onetwo[y][a] = one[y][i]
                a += 1
            for i in range(len(two[0])):
                onetwo[y][a] = two[y][i]
                a += 1
        print(onetwo)
        return onetwo

    def makeClockLayout(self, w, h, number):
        nl = self.__numList(number)
        # mark notates the location to add an extra vertical space 
        mark = len(nl) - 2
        toRet = [[]] * h 
        #print("| nl ~ length ~ " + str(len(nl)) + " |     | nl is " + str(nl) + " |")
        #print(toRet)
        columnArray = np.full((h, 1), False)
        for i in range(len(nl)):
            #print("Number to add next: " + str(nl[i]))
            nextNumberArray = self.__makeNumber(w,h,nl[i])
            toRet = self.__combineMatrices(toRet, nextNumberArray)
            #print(str(i) + " toReturn 1")
            #print(toRet)
            # Space Between Numbers
            if not i == len(nl) - 1:
                toRet = self.__combineMatrices(toRet, columnArray)
            #print(toRet)
            #print(str(i) + " toReturn 2")
            # Additional Space for Between Hours and Minutes
            if i == mark - 1:
                toRet = self.__combineMatrices(toRet, columnArray)
        return toRet

    def __numList(self, number):
        numList = []
        while (0 < number):
            a = int(number % 10)
            number = (number - a) / 10 
            numList.insert(0, a)
        return numList

    def __makeNumber(self, w, h, number):
        numArray = np.full((h, w), False)
        linesToFill = self.__getSegments(number)
        #print(number)
        #print(linesToFill)
        for index in range(len(linesToFill)):
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
                numArray[x][y] = True
                #print("(x " + str(x) + ", y " + str(y) + ")")
        return numArray

    # Print 2d Boolean Array as 1s and 0s
    def printBoolArr(self, arr):
        w = len(arr[0])
        h = len(arr)
        numArray = np.full((h, w), 0)
        for x in range(w):
            for y in range(h):
                if arr[y][x]:
                    numArray[y][x] = 1
        print("Printed Bool Array")
        print(numArray)
        print()

if __name__ == '__main__':
    tim = tim.timer()
    ani = ani.animation(16, 16)
    rc = run_clock(tim, ani)

    print()
    print([[0] * 3]* 5)
    print()

    w = 3
    h = 8
    
    for i in range(-1, 10):
        pass
        #rc.printDigit(w, h, i)
    number = 1135
    digitalFace = rc.makeClockLayout(3, 8, 1135)
    print("")
    print("Booleans")
    print(digitalFace)
    print("Numbers")
    rc.printBoolArr(digitalFace)

