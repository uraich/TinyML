# plotStrokeRaster.py: Reads the binary raster image and plots it
# Copyright (c) U. Raich, March 2026
# This program is part of the TinyML course at the University of Cape Coast, Ghana
# It is released under the MIT license

# Read the image file
from micropython import const
from rasterize import plotStroke, RASTER_WIDTH,RASTER_HEIGHT,RASTER_WIDTH
from time import sleep

for i in range(10):
    filename = "samples/{:d}.bin".format(i)
    print(filename)

    imgFile = open(filename,"rb")    # read binary file
    rasterImg = imgFile.read()
    print(len(rasterImg))
    for j in range(15):
        print("0x{:02x},".format(rasterImg[j]),end="")
    print("0x{:02x}".format(rasterImg[15]))   
    
    plotStroke(rasterImg)

    sleep(1)