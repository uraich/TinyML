# magic_wand_ble_led_from_file.py: Reads a json file with stroke data for each digit
# Rasterized the stroke and prints it.
# This program tests the rasterization algorithm
# Copyright (c) U. Raich Jan 2026
# This program is part of the TinyML course at the
# University of Cape Coast, Ghana
# It is released under the MIT license

import sys
from micropython import const
import json, math
from time import sleep_ms
from rasterize import rasterizeStroke,RASTER_WIDTH,RASTER_HEIGHT,RASTER_CHANNELS,RANGE_X,RANGE_Y

# gets the stroke points for a particular digit

def findStroke(digit_no):
    for i in range(10):
        if strokes["strokes"][i]["label"] == str(digit_no):
            print("Stroke {:d} found!".format(digit_no))
    return strokes["strokes"][digit_no]["strokePoints"]

def toFloatArray(strokePoints):
    # takes stroke points in form of dictionaries:
    # {"x": "x_value","y": "y_value"}
    # and converts them into a list of float values of the form:
    # x0_value,y0_value,x1_value,y1_value ...
    pointArray = []
    for i in range(len(strokePoints)):
        pointArray.append(float(strokePoints[i]["x"]))
        pointArray.append(float(strokePoints[i]["y"]))
    return pointArray
    
          
# Read the json file with 10 digit example strokes
try:
    jsonFile = open("strokes/digits.json","r")
    strokes = json.load(jsonFile)
except:
    print("Please make sure that digits.json has been uploaded to /strokes")
    sys.exit()
    
# get at the stroke points

for digit in range(10):
    strokePoints = findStroke(digit)
    pointArray = toFloatArray(strokePoints)
    # print("x0: {:5.3f}, y0: {:5.3f}".format(pointArray[0],pointArray[1]))
    rasterBuffer = rasterizeStroke(pointArray, RANGE_X, RANGE_Y, RASTER_WIDTH, RASTER_HEIGHT)
    '''
    print("Colors:")
    for i in range(4):
        for j in range(3):
            print("({:d},{:d},{:d}), ".format(rasterBuffer[3*i*4 + 3*j],
                                              rasterBuffer[3*i*4 + 3*j+1],
                                              rasterBuffer[3*i*4 + 3*j+2]),end="")
            
            print("({:d},{:d},{:d})".format(rasterBuffer[3*i*4 + 3*3],
                                            rasterBuffer[3*i*4 + 3*3+1],
                                            rasterBuffer[3*i*4 + 3*3+2]))
    '''                                        
                                              
    for y in range(RASTER_HEIGHT):
        line = ""
        for x in range(RASTER_WIDTH):
            pixel_index = y * RASTER_WIDTH * RASTER_CHANNELS + x * RASTER_CHANNELS
            red = rasterBuffer[pixel_index]
            green = rasterBuffer[pixel_index+1]
            blue = rasterBuffer[pixel_index+2]

            if red > 0 or green > 0 or blue > 0:
                line += '#'
            else:
                line +='.'
        print(line)
    sleep_ms(3000)
