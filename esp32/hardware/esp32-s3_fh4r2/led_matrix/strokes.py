# strokes.py: switches the pixels on the matrix to show "W", "O" and "L"
# These are the strokes on the original magic wand demo
# I take into account that the magic wand is vertical, which means that
# the matrix is turned be 90°
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

W = [0x1f,0x40,0x80,0x20,0x20,0x80,0x40,0x1f]
L = [0x00,0x00,0x40,0x40,0x40,0x7f,0x00,0x00]
O = [0x18,0x24,0x42,0x81,0x81,0x42,0x24,0x18]
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

def showLetter(letter):
    for columns in range(NO_OF_COLS):
        mask = 1
        pixels = letter[columns]
        for rows in range(NO_OF_ROWS):
            if (pixels & mask):
                led_on(columns*NO_OF_COLS + rows)
            else:
                led_off(columns*NO_OF_COLS + rows)
            mask <<= 1
            
try:
    showLetter(W)
    sleep_ms(2000)
    showLetter(L)
    sleep_ms(2000)
    showLetter(O)
    sleep_ms(2000)
    switchAll_LedsOff()    
        
except KeyboardInterrupt:
    switchAll_LedsOff()
