# ws2812_intens.py: increases, then decreases the light intensity on the
# neopixel of the esp32-s3 board.
# Copyright (c) U. Raich 11. Oct. 2023
# This program is part of the course on tinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms
import sys

def led_off():
    neopixel[0] = (0,0,0)
    neopixel.write()
    
# check if  the hardware definition file is already loaded
try:
    from hw_esp32_s3_fh4r2 import *
except:
    print("Please make sure hw_esp32_s3_fh4r2.py has been uploaded to /lib")
    sys.exit()

# NEOPIXEL and NO_OF_NEOPIXELS is defined in the hardware definition file hw_esp32_s3_fh4r2.py
neopixel = NeoPixel(Pin(NEOPIXEL),NO_OF_NEOPIXELS)
maxIntensity = 100

try:
    while True:
        
        for intens in range(maxIntensity):
            neopixel[0] = (0,0,intens)
            neopixel.write()
            sleep_ms(20)
        for intens in range(maxIntensity,0,-1):        
            neopixel[0] = (0,0,intens)
            neopixel.write()
            sleep_ms(20)
            
except KeyboardInterrupt:
    led_off()

    
