# Helps with generic remapping of array elements
import copy

class array_manipulator:
    def __init__(self):
        pass
    
    ## Swap Number
        # Takes in array 'arr' and replace all instances of 'a' with 'b'.
    def swapNumber(self, arr, a, b):
        if not len(arr) == len(boolArr) or not (len(arr[0]) == len(boolArr[0])):
            raise NamError('arrays given not the same dimensions') 
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

if __name__ == '__main__':