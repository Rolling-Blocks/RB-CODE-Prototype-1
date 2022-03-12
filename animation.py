import skimage
from skimage import color
from skimage import io
import numpy as np
import time
import cv2
import copy
from disp_def import DispDef as DD 
from disp_def import blockStateKey
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
        difs = self._getDifOfRows(diffArr)
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
        offsetWithChange = self._getDifOfRows(changed)
        #print("offsetWithChange     " + str(offsetWithChange))
        offsetWithoutChange = self._getDifOfRows(diffArr)
        #print("offsetWithoutChange  " + str(offsetWithoutChange)) 

        changeHelp = []
        for row in range(0,len(diffArr)):
            if offsetWithChange[row] < offsetWithoutChange[row]:
                changeHelp.append(row)
        #print("Change Help " + str(changeHelp))
        return changeHelp

    def makeMoveQue(self):
        diffArr = copy.deepcopy(self._findDifMat())
        moveQue = []
        while(True):
            change = copy.deepcopy(diffArr[self._leastDifRow(diffArr)])
            unlock = self._changeHelpRow(diffArr, change) 
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

    def getGcode(self):
        
        mq = self.makeMoveQue()
        moves = []

        # Row Lock
        rowReMove = DD.ROWLOCK
        rowReActuateTo = [DD.LOCK] * self.dispHeight
        moves.append([rowReMove, rowReActuateTo])

        for i in range(0, len(mq)):
            # Column Return
            colRetMove = DD.COLRETURN
            colRetActuateTo = []
            for x in range(0, self.dispWidth): 
                if not mq[i][0][x] == 2:
                    colRetActuateTo.append(DD.MIDDLE)
                else:
                    colRetActuateTo.append(DD.SUBTRACT)
            moves.append([colRetMove, colRetActuateTo])

            # Row Unlocks
            rowUnMove = DD.ROWUNLOCK
            rowUnActuateTo = [DD.LOCK] * self.dispHeight
            for x in range(0, len(mq[i][1])):
                rowUnActuateTo[mq[i][1][x]] = DD.UNLOCK
            moves.append([rowUnMove, rowUnActuateTo])

            # Column Actuate
            colActMove = DD.COLACTUATE
            # Odds
            colActActuateTo = []
            for x in range(0, len(mq[i][0])):
                if x % 2 == 1:
                    colActActuateTo.append(colRetActuateTo[x])
                else:
                    if mq[i][0][x] == -1:
                        colActActuateTo.append(DD.SUBTRACT)
                    if mq[i][0][x] == 0:
                        colActActuateTo.append(DD.MIDDLE)
                    if mq[i][0][x] == 1 or mq[i][0][x] == 2:
                        colActActuateTo.append(DD.ADD)
            moves.append([colActMove, colActActuateTo])
            # Evens
            colActActuateTo = []
            for x in range(0, len(mq[i][0])):
                if mq[i][0][x] == -1:
                    colActActuateTo.append(DD.SUBTRACT)
                if mq[i][0][x] == 0:
                    colActActuateTo.append(DD.MIDDLE)
                if mq[i][0][x] == 1 or mq[i][0][x] == 2:
                    colActActuateTo.append(DD.ADD)
            moves.append([colActMove, colActActuateTo])

            # Row Lock
            rowReMove = DD.ROWLOCK
            rowReActuateTo = [DD.LOCK] * self.dispHeight
            moves.append([rowReMove, rowReActuateTo])
        return moves

    def printGcode(self, gcode):
        for i in range(0 , len(gcode)):
            strang = ""
            if gcode[i][0] is DD.ROWLOCK:
                strang += "ROW LOCK"
            if gcode[i][0] is DD.COLRETURN:
                strang += "COL RETURN"
            if gcode[i][0] is DD.ROWUNLOCK:
                strang += "ROW UNLOCK"
            if gcode[i][0] is DD.COLACTUATE:
                strang += "COL ACTUATE"
            print("")
            print(strang)

            strang = ""
            for j in range(0, len(gcode[i][1])):
                if not j == 0:
                    strang += ", "
                if gcode[i][1][j] == DD.LOCK:
                    strang += "LOCK"
                if gcode[i][1][j] == DD.UNLOCK:
                    strang += "UNLK"
                if gcode[i][1][j] == DD.SUBTRACT:
                    strang += "SUB"
                if gcode[i][1][j] == DD.MIDDLE:
                    strang += "MID"
                if gcode[i][1][j] == DD.ADD:
                    strang += "ADD"
            print(strang)

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
    diff = a._findDifMat()
    ldRow = a._leastDifRow(diff)

    print("diff")
    print(diff)

    mq = a.makeMoveQue()
    a.printMq(mq)
    gg = a.getGcode()
    a.printGcode(gg)

    i = 1
    while True:
        time.sleep(1)
        i += 1

    