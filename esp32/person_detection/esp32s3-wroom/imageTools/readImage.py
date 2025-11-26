# Reads a 96x96 pixel gray scale image from the camera in raw mode
# This image can directly be passed into the input tensor of the
# person detection model
# The program is part of a course on AI and edge computing at the
# University of Cape Coast, Ghana
# Copyright (c) U. Raich [2022]
# The program is released under the MIT License

import sys
import camera
from utime import sleep_ms

try:
    # this is for the esp32-cam-mb using ov2640 sensor
    # camera.init(0,format=camera.GRAYSCALE,framesize=camera.FRAME_96X96)
    # switch to this for the m5 timer camera with ov3660 sensor
    # camera.init(0,format=camera.GRAYSCALE,framesize=camera.FRAME_96X96,
                # sioc=23,siod=25,xclk=27,vsync=22,href=26,pclk=21,
                # d0=32,d1=35,d2=34,d3=5,d4=39,d5=18,d6=36,d7=19,
                # reset=15)
    # ... and this one for the FreeNove ESP32S3-WROOM
    camera.init(0,d0=11, d1=9, d2=8, d3=10, d4=12, d5=18, d6=17, d7=16,
                format=camera.GRAYSCALE, framesize=camera.FRAME_96X96, 
                xclk_freq=camera.XCLK_20MHz,
                href=7, vsync=6, reset=-1, pwdn=-1,
                sioc=5, siod=4, xclk=15, pclk=13)    
except:
    print("Error when initializing the camera")
    sys.exit()
    
buf=camera.capture()
print("type: ", type(buf), " Length: ",len(buf))
# save the raw image to a file
print("Writing the data to camImage.raw")
if len(buf) == 96*96:
    f = open("camImage.raw","w+b")
    f.write(buf)
    f.close()
    
camera.deinit()
