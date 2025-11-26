#!/usr/bin/python3
# extractPixelsFromPNG.py extracts the RGB pixel values from a png
# image file and write them onto a binary file
# Copyright (c) U. Raich
# This program if part of the TinyML course at the
# University of Cape Coast, Ghana
# It is releaased under the MIT license

from PIL import Image
import numpy as np
import sys,os

if len(sys.argv) != 2:
    print("Usage: {:s} png filename".format(sys.argv[0]))
    sys.exit()

filename = sys.argv[1]

im = Image.open(filename)
im.convert('RGB')
imageSizeW, imageSizeH = im.size
print("image width: {:d}, image height: {:d}".format(imageSizeW, imageSizeH))
pixels = np.array(im).reshape((32,32,3))
print("shape of stroke array: ",pixels.shape)
print("dtype of stroke pixels: ",pixels.dtype)4

# convert to int8_t as expected by the model
pixels = (pixels-128).astype(np.int8)
print("dtype after conversion to int8: ",pixels.dtype) 
print("min pixel value: {:d}, max pixel_value: {:d}".format(np.min(pixels),np.max(pixels)))

output_filename = os.path.splitext(filename)[0] + ".bin"
print("Binary file saved to {:s}".format(output_filename))
f = open(output_filename,"wb")
f.write(pixels)
f.close()
