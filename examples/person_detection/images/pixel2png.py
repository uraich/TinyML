#!/usr/bin/python3
from PIL import Image
import numpy as np
import sys
import os

if len(sys.argv) != 2:
    print("Usage: {} filename of pixel file".format(sys.argv[0]))
    sys.exit()

# read the pixels from a raw pixel file
# the pixels are gray scale with signed int8 pixel values

filename = sys.argv[1]
f = open(filename,'rb')
pixels = bytearray()
pixels = f.read()
f.close()

print("size of pixel array: {:d}".format(len(pixels)))
if len(pixels) != 96*96:
    print("Error when reading the pixel file")
    print("It must be 96*96 int8 values")
    sys.exit()

pixels = np.frombuffer(pixels,dtype=np.int8).reshape((96,96))
image = Image.fromarray(pixels,mode='L')
filename = os.path.splitext(sys.argv[1])[0]
image.save(filename + ".png")
