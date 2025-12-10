# Reads a 96x96 pixel jpeg image from the camera 
# This image can easily be displayed with an image viewer
# The program is part of a course on AI and edge computing at the
# University of Cape Coast, Ghana
# Copyright (c) U. Raich, Dec 2025
# The program is released under the MIT License

import sys
import camera
from utime import sleep_ms

try:
    from hw_esp32_s3_fn8 import *
except:
    print("Please make sure hw_esp32_s3_fn8.py has been uploaded to /lib")
    sys.exit()
# make sure the camera is not already initialized, which would provoke an error    
camera.deinit()    
cam_init_result = camera.init(0, d0=CAM_D0, d1=CAM_D1, d2=CAM_D2, d3=CAM_D3,
                              d4=CAM_D4, d5=CAM_D5, d6=CAM_D6, d7=CAM_D7,
                              format=camera.JPEG, framesize=camera.FRAME_VGA, 
                              xclk_freq=camera.XCLK_20MHz,
                              href=CAM_HREF, vsync=CAM_VSYNC,
                              reset=CAM_RESET, pwdn=CAM_PWDN,
                              sioc=CAM_SIOC, siod=CAM_SIOD,
                              xclk=CAM_XCLK, pclk=CAM_PCLK)

if cam_init_result:
    print("Running on the esp32s3-fn8_cam board")
    print("Camera was successfully initialized")
else:
    print("Camera initialization failed");

# set framesize to 96x96 pixels
camera.set_framesize(camera.FRAME_96X96)

# increase the brightness, which is -2 in case of grayscale images
camera.set_brightness(0)

buf=camera.capture()
try:
    print("type: ", type(buf), " Length: ",len(buf))
    # save the raw image to a file
    print("Writing the data to images/camImage.jpg")
    if len(buf) > 0:
        f = open("images/camImage.jpg","w+b")
        f.write(buf)
        f.close()
except:
    if not buf:
        print("Failure reading image file")
        print("Try to un-power and re-power the esp32s3-fn8_cam board")
    
camera.deinit()
