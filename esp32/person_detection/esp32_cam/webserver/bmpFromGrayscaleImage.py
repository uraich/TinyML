# createBmp.py: Reads an image from the esp32s3-fn8_cam, converts it into a
# bmp image and saves it onto a file
# This is the first stage before integrating grayscale image reading into
# a streaming web server
# Copyright (c) U. Raich, Dec 2025
# This program is part of the course on TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

import sys
import camera
import struct

try:
    from hw_esp32_s3_fn8 import *
except:
    print("Please make sure hw_esp32_s3_fn8.py has been uploaded to /lib")
    sys.exit()

# Disable camera initialization
camera.deinit()

# Enable camera initialization
print("We are on the ESP32-S3-FN8")

cam_init_result = camera.init(0, d0=CAM_D0, d1=CAM_D1, d2=CAM_D2, d3=CAM_D3,
                              d4=CAM_D4, d5=CAM_D5, d6=CAM_D6, d7=CAM_D7,
                              format=camera.GRAYSCALE,
                              framesize=camera.FRAME_96X96, 
                              xclk_freq=camera.XCLK_20MHz,
                              href=CAM_HREF, vsync=CAM_VSYNC,
                              reset=CAM_RESET, pwdn=CAM_PWDN,
                              sioc=CAM_SIOC, siod=CAM_SIOD,
                              xclk=CAM_XCLK, pclk=CAM_PCLK)

if cam_init_result:
  print("Camera was successfully initialized")
else:
  print("Camera initialization failed");
  sys.exit(-1)

print("Flipping the image vertically. The bmp file starts from the bottom")
camera.set_vflip(True)

# Create the headers and palette needed to transform the grayscale video
# image info a bmp file
# start with the info header

BI_RGB = 0
infoHeader = bytearray(40)
infoHdrSize = len(infoHeader)
imageWidth = 96
imageHeight = 96
noOfPlanes = 1
noOfBitsPerPixel = 8
compression = BI_RGB                    # no compression
imageSize = 0                           # this works for uncompressed images
imageSize = imageWidth * imageHeight * 2
hor_resolution = 0                      # no preference
ver_resolution = 0                      # no preference
noOfColors = 256                        # only used with color maps
importantColors = 0
infoHdr = struct.pack("3i2h6i",infoHdrSize,imageWidth,imageHeight,noOfPlanes,
                      noOfBitsPerPixel,compression,imageSize,
                      hor_resolution,ver_resolution,
                      noOfColors,importantColors)

# Now the color palette
palette = bytearray(256*4)
for i in range(256):
    palette[4*i]   = i
    palette[4*i+1] = i
    palette[4*i+2] = i
    palette[4*i+3] = 0xff

# ...and finally the file header
fileHdrSize = 14
magic = 'BM'.encode('ascii')
fileSize = fileHdrSize + len(infoHdr) + len(palette) + 96*96
reserved = 0
offset = fileHdrSize + len(infoHdr) + len(palette)
hdr = magic + struct.pack('ihhi',fileSize,reserved,reserved,offset)

# From now on, all we need is the data from the camera
pixel_data = camera.capture()
if not len(pixel_data) == 96*96:
    print("problem reading the image from the camera")
    sys.exit(-1)

# concatenate file header, info header, palette and pixel_data and write the bmp file
frame = hdr + infoHdr + palette + pixel_data

print("Writing the file camera.bmp")
bmpFile = open("camera.bmp","wb")
bmpFile.write(frame)
bmpFile.close()
