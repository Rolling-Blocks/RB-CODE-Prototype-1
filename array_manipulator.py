# Helps with generic remapping of array elements
import copy
import numpy as np

class array_manipulator:
    def __init__(self):
        pass
    
    ## Swap Number
        # Takes in array 'arr' and replace all instances of 'a' with 'b'.
    def swapNumber(self, arr, a, b):
        arrCop = copy.deepcopy(arr)
        for j in range(len(arr)):
            for i in range(len(arr[0])):
                if arr[j][i] == a:
                    arrCop[j][i] = b
        return arrCop

    ## Bool Map
        # Takes in 2d array 'arr' and boolean array 'boolArr' of the same size
        # All elements of 'arr' where the corresponding element in 'boolArr' is true are replaced with 'a'
    def boolMap(self, arr, boolArr, a):
        if not len(arr) == len(boolArr) or not (len(arr[0]) == len(boolArr[0])):
            raise NamError('arrays given not the same dimensions') 
        arrCop = copy.deepcopy(arr)
        for j in range(len(arr)):
            for i in range(len(arr[0])):
                if boolArr[j][i]:
                    arrCop[j][i] = a
        return arrCop

    def addArray(self, arr1, arr2, modBy = -1):
        if not len(arr1) == len(arr2) or not (len(arr1[0]) == len(arr2[0])):
            raise NamError('arrays given not the same dimensions') 
        arrBlank = np.zeros((len(arr1), len(arr1[0])))
        for j in range(len(arrBlank)):
            for i in range(len(arrBlank[0])):
                arrCop[j][i] = arr1[j][i] + arr2[j][i]
                if not modBy == -1:
                    arrCop[j][i] = arrCop[j][i] % modBy
        return arrCop

    ## Increment By
        # Takes all elements of 'arr' greater than 'a' and less then 'b'
    def incrementArrBy(self, arr, a, b, modBy = -1):
        arrCop = copy.deepcopy(arr)
        for j in range(len(arr)):
            for i in range(len(arr[0])):
                if a <= arr[j][i] and arr[j][i] <= b:
                    if modBy == -1:
                        arrCop[j][i] = (arrCop[j][i] + 1) % (b + 1)
                    if not modBy == -1:
                        arrCop[j][i] = (arrCop[j][i] + 1) % modBy
        return arrCop



if __name__ == '__main__':
    am = array_manipulator()
    dispDim = (10,6)
    init =  np.random.randint(0, 6, size=dispDim)
    print(init)
    b = [True, False, False]
    boolArr = np.random.choice(b, size=dispDim)
    #print(boolArr)
    #print(am.swapNumber(init, 2, 3))
    #print(am.boolMap(init, boolArr, -1))
    print(am.incrementArrBy(init, 4, 5))