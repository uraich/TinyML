# strokes.py: switches the pixels on the matrix to show digits  0..9
# These are the strokes on the original magic wand demo
# I take into account that the magic wand is vertical, which means that
# the matrix is turned be 90°
# Copyright (c) U. Raich 21. dec. 2025
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

zero  = [0x00,0x1c,0x22,0x41,0x41,0x22,0x1c,0x00] 
one   = [0x00,0x40,0x40,0x7f,0x42,0x44,0x00,0x00]
two   = [0x00,0x46,0x49,0x51,0x62,0x40,0x00,0x00]
three = [0x00,0x00,0x36,0x49,0x49,0x22,0x00,0x00]
four  = [0x00,0x40,0x48,0x7f,0x4a,0x4c,0x08,0x00]
five  = [0x00,0x00,0x31,0x49,0x49,0x4f,0x00,0x00]
six   = [0x00,0x00,0x31,0x49,0x4a,0x3c,0x00,0x00]
seven = [0x00,0x07,0x09,0x11,0x21,0x41,0x00,0x00]
eight = [0x00,0x00,0x36,0x49,0x49,0x36,0x00,0x00]
nine  = [0x00,0x00,0x3e,0x49,0x49,0x46,0x00,0x00]

digits = { 0: zero,
           1: one,
           2: two,
           3: three,
           4: four,
           5: five,
           6: six,
           7: seven,
           8: eight,
           9: nine}

NO_OF_ROWS = const(8)
NO_OF_COLS = const(8)

ON         = 1
OFF        = 0

led = NeoPixel(Pin(MATRIX), NO_OF_MATRIX_LEDS)

def switchAll_LedsOff():
    for led_no in range(NO_OF_MATRIX_LEDS):
        led[led_no] = (0,0,0)
    led.write()
        
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

def showDigit(digit):
    for columns in range(NO_OF_COLS):
        mask = 1
        pixels = digits[digit][columns]
        print("pixels: 0x{:02x}".format(pixels))
        for rows in range(NO_OF_ROWS):
            if (pixels & mask):
                led_on(columns*NO_OF_COLS + rows)
            else:
                led_off(columns*NO_OF_COLS + rows)
            mask <<= 1
            
try:
    for i in range(10):
        showDigit(i)
        sleep_ms(2000)
    switchAll_LedsOff()    
        
except KeyboardInterrupt:
    switchAll_LedsOff()
