# blink.py: blinks the flash light at 1 Hz
# The flash LED is connected to GPIO 4. At its max light intensity it is
# extremely bright. For this reason we turn down the intensity to 20%
# of its maximum using PWM
# Copyright (c) U. Raich, Mar, 2024
# This program is part of a course on tinyML for the
# African Internet Summit 2024
# It is released under the MIT license

import sys
from time import sleep_ms
from machine import Pin,PWM

def percent2Duty(percent):
    return 1024*percent//100

def flashOn(percent):
    flash.duty(percent)
    dutyCycle = percent2Duty(percent)
    # print("Intensity: ",percent)
    # print("Duty cycle: ",dutyCycle)


def flashOff():
    flash.duty(0)
    
try:
    from hw_esp32_cam import FLASH, INTENSITY
except:
    print("Please make sure hw_esp32_cam.py has been uploaded to /lib")
    sys.exit()

flashPin = Pin(FLASH,Pin.OUT)  #create LED object from pin4, Set Pin4 to output
flash = PWM(flashPin)

try:
    while True:
        flashOn(INTENSITY)  # Turn flash light on
        sleep_ms(500)
        flashOff()           # Turn flash light off
        sleep_ms(500)
except:
    pass




