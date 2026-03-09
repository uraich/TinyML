#!/home/uli/.virtualenvs/AI-Pythonv3.12/bin/python
# Read all 10 digit files into a dictionary, with the same structure as
# Pete Warden's magic word data files and dump it into a json file
# This json file can be transfered to the ESP32 and read back there.
# The stroke data can then be communicated to a WEB page and plotted there
# 
# This allows to reconstruct the way Pete Warden uses to transfer stroke
# data to his WEB page when acquiring training data
#
# Copyright (c) U. Raich
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

import json
import matplotlib as plt

# read a digit.txt file and extract x,y and label

def readStrokeFile(filename):
    strokeFile = open(filename,"r")
    strokeData = strokeFile.read()
    strokeFile.close
    # extract the digit number from the filename
    label = filename.replace("digit_","")
    label = label.replace(".txt","")
    # print("label: ",label)
    # stroke _data now contains a string with stroke points
    x = []
    y = []
    strokePoints = strokeData.split("\n")
    for i in range(len(strokePoints)):
        # the file has a closing \n, which results in an empty line
        if strokePoints[i] != "":
            tmp = strokePoints[i].split(" ")
            x.append(tmp[0])
            y.append(tmp[1])         
    return (label,x,y)

# Create a dictionary into which the data will be sorted and which
# will be dumped into a json file

strokeDict = {"strokes" : []}

# Read all 10 digit files and sort the data into the dictionary

for i in range(10):
    strokeFilename = "digit_{:d}.txt".format(i)  # create the digit filename
    entry = readStrokeFile(strokeFilename)
    strokeDict["strokes"].append({"index":i,"strokePoints":[],"label":entry[0]})
    for j in range(len(entry[1])):  # go over all x and y values and fill them into the dictionary
        strokeDict["strokes"][i]["strokePoints"].append({"x":entry[1][j],"y":entry[2][j]})

# Finally we write the dictionary to a file

with open("digits.json","w") as jsonFile:
    json.dump(strokeDict,jsonFile)
