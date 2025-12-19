# pixel_pos.py: switches each pixel on the matrix on for some 200 ms
# Copyright (c) U. Raich 18. dec. 2025
# This program is part of the course on tinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms
import sys
try:
    from hw_esp32_s3_fh4r2 import *
except:
    print("Please make sure hw_esp32_s3_fh4r2.py has been uploaded to /lib")
    sys.exit()

ON         = 1
OFF        = 0

led = NeoPixel(Pin(MATRIX), NO_OF_MATRIX_LEDS)

def switchAll_LedsOff():
    for led_no in range(NO_OF_MATRIX_LEDS):
        led_off(led_no)
        
def switchLED(led_no,onOff):
    if onOff:
        led[led_no] = (0,0,INTENSITY)   # blue
    else:
        led[led_no]  = (0,0,0)
    led.write()

def led_on(led_no):
    switchLED(led_no,ON)
    
def led_off(led_no):
    switchLED(led_no,OFF)

try:
    while True:
        # switch each of the LEDs on for 200 ms
        # switch it off after
        for led_no in range(NO_OF_MATRIX_LEDS):
            led_on(led_no)
            sleep_ms(200)
            led_off(led_no)
            sleep_ms(200)
        
except KeyboardInterrupt:
    switchAll_LedsOff()
