# clearFlash: switches the flash light off
# The flash LED is connected to GPIO 4. 
# Copyright (c) U. Raich, Mar, 2024
# This program is part of a course on tinyML for the
# African Internet Summit 2024
# It is released under the MIT license

import sys
from machine import Pin,PWM

def flashOff():
    flash.duty(0)
    
try:
    from hw_esp32_cam import FLASH
except:
    print("Please make sure hw_esp32_cam.py has been uploaded to /lib")
    sys.exit()

flashPin = Pin(FLASH,Pin.OUT)  #create LED object from pin4, Set Pin4 to output
flash = PWM(flashPin)

flashOff()           # Turn flash light off





