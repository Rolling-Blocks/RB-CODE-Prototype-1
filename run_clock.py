# Checkboard BackDrop
# Shows Time in Hours and Minutes Like Classic Analog Clock

import time
import random
from disp_def import DispDef, blockStateKey
import image_processor as impr
import display_virtual as disvir
import timer as tim
import numpy as np
import copy

class run_clock:
    def __init__(self, t):
        self.timmo = t

    def getClockGcode(self, blankBackground):
        pass

    def getClockArray(self, w = 3, h = 8, number = -1):
        if number == -1:
            n = self.timmo.getNow()
        else:
            n = number
        return self.__makeClockLayout(w, h, n)

    # Used to cut falses off the left side of the array
    def cutBloat(self, array):
        go = True
        i = 0
        j = 0
        upToColumnCut = -1
        while go and (i < len(array[0])):
            while go and (j < len(array)) 
                if array[j][i]: 
                    go = False
                j += 1
            # If Column Completely False Cut Column
            if go:
                upToColumnCut = i
            i += 1
        
        # Cut Up To Column i

    def printDigit(self, w, h, number):
        num = self.__makeNumber(w, h, number)
        self.printBoolArr(num)

    def printClock(self, w, h, number):
        digitalFace = self.__makeClockLayout(w, h, number)
        self.printBoolArr(digitalFace)

    def __makeClockLayout(self, w, h, number):
        nl = self.__numList(number)
        # mark notates the location to add an extra vertical space 
        mark = len(nl) - 2
        toRet = [[]] * h 
        columnArray = np.full((h, 1), False)
        for i in range(len(nl)):
            nextNumberArray = self.__makeNumber(w,h,nl[i])
            toRet = self.__combineMatrices(toRet, nextNumberArray)
            if not i == len(nl) - 1:
                toRet = self.__combineMatrices(toRet, columnArray)
            if i == mark - 1:
                toRet = self.__combineMatrices(toRet, columnArray)
        return toRet

    def __combineMatrices(self, one, two):
        onetwo = [[0] * (len(one[0]) + len(two[0])) for i in range(len(one))]
        for y in range(len(one)):
            a = 0
            for i in range(len(one[0])):
                onetwo[y][a] = one[y][i]
                a += 1
            for i in range(len(two[0])):
                onetwo[y][a] = two[y][i]
                a += 1
        #print(onetwo)
        return onetwo

    def __numList(self, number):
        numList = []
        while (0 < number):
            a = int(number % 10)
            number = (number - a) / 10 
            numList.insert(0, a)
        return numList

    # Makes Array of Individual Digits
    def __makeNumber(self, w, h, number):
        numArray = np.full((h, w), False)
        linesToFill = self.__getSegments(number)
        for index in range(len(linesToFill)):
            segmentNum = linesToFill[index]
            sd = self.__numToSegment(w, h, segmentNum)
            segmentArr = self.__fillLine(w, h, sd[1], sd[0])
            numArray = np.logical_or(numArray, segmentArr)
        
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
    rc = run_clock(tim)

    w = 3
    h = 8
    
    for i in range(-1, 10):
        pass
        #rc.printDigit(w, h, i)
    number = -1
    while True:
        if tim.beenMinute():
            digitalFace = rc.getClockArray(w, h, number)
            rc.printBoolArr(digitalFace)

