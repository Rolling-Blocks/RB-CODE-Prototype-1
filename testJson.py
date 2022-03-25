# Python program to demonstrate
# Conversion of JSON data to
# dictionary
#
 
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