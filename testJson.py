# Python program to demonstrate
# Conversion of JSON data to
# dictionary
 
# importing the module
import json

# Opening JSON file
with open('display_16x16.json') as json_file:
    data = json.load(json_file)

# Print the type of data variable
print("Type:", type(data))
 
# Print the data of dictionary
print("\nr0:", data['r0']['moduleId'])
print("\nr1:", data['r1'])
print("\nr2:", data['r2'])
print("\nr3:", data['r3'])
print("\nr4:", data['c4'])
arr = [0 for i in range(16)]
print(arr)
arr[5] = 5
print(arr)
print()
double = lambda x : x * 2
inBounds = lambda a : max(0, min(255, int(a * 255)))
print([double(i) for i in (10, 5)])
print("testing in bouinds")
print(inBounds(1.01))

def my_function(fname): print(fname + " Refsnes")
my_function("sedrrt")

print(data)