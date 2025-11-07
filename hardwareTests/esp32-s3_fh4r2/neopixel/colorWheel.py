# colorwheel.py:  Shows all the colors of the rainbow on the NeoPixel LEDs
# 
# Copyright U. Raich 2022
# The program is part of African School of Physics 2022
# Released under the MIT license

import sys
from utime import sleep_ms
from machine import Pin
from neopixel import NeoPixel
try:
    from hw_esp32_s3_fh4r2 import NEOPIXEL, NO_OF_NEOPIXELS, INTENSITY
except:
    print("Please make sure hw_esp32_s3_fh4r2.py has been uploaded to /lib")
    sys.exit()

# We set the max LED intensity to 31 in order not to blind our eyes
MAX_INTENSITY = INTENSITY

# these are the color components (used only for printing)
RED = 1
GREEN = 0
BLUE = 2

dark = (0,0,0)

# clears all the LEDs
# this is used to switch off all the LEDs when we terminate the program with ^C
def clear():
    # clear all the LEDs
    for i in range(NO_OF_NEOPIXELS):
        neopixel[i]=dark
        neopixel.write()

# init the NeoPixel driver
neopixel = NeoPixel(Pin(NEOPIXEL),NO_OF_NEOPIXELS)

# if you observe the color wheel very attentively then you see that there is only one color component that
# is changing as we go around the ring.
# 0°..60°:     red is constantly at max, blue is constantly zero and green increases
# 60°.. 120°:  green is constantly at max, blue is zero and red decreases
# similar for all the 6 sectors
# We must therefore check in which sector the angular position is falling, then we can easily calculate
# the color components depending on the angular position around the ring

def colors(pos):
    if pos<60:
        red=MAX_INTENSITY
        green=int(MAX_INTENSITY*pos/60)
        blue=0
    elif pos >=60 and pos < 120:
        red=MAX_INTENSITY-int(MAX_INTENSITY*(pos-60)/60)
        green = MAX_INTENSITY
        blue = 0
    elif pos >=120 and pos < 180:
        red = 0
        blue = int(MAX_INTENSITY*(pos-120)/60)
        green = MAX_INTENSITY
    elif pos >= 180 and pos < 240:
        red = 0
        green = MAX_INTENSITY-int(MAX_INTENSITY*(pos-180)/60)
        blue = MAX_INTENSITY
    elif pos >= 240 and pos < 300:
        red = int(MAX_INTENSITY*(pos-240)/60)
        green = 0
        blue = MAX_INTENSITY
    else:
        red = MAX_INTENSITY
        green = 0
        blue = MAX_INTENSITY - int(MAX_INTENSITY*(pos-300)/60)

    return (green,red,blue)
             

def show(color):
    for i in range(NO_OF_NEOPIXELS):
        neopixel[i] = color
    neopixel.write()
    sleep_ms(100)

def print_colors(color):
    print("red: {:03d}, green: {:03d}, blue: {:03d}".format(color[RED],color[GREEN],color[BLUE]))
        
print("color wheel running on ",sys.platform)

printFlag = True
# We go around the 360° of the color wheel in clockwise direction. This means, we start with red the go to
# yellow, green, cyan, blue ...
# We print the color components for verification only the first time we go around the wheel.

# the try - except clause is used to clear the LEDs when we stop the program with ^C
# we did not discuss this during the lectures
try:
    while True:
        # we go in steps of 2 degrees to speed up the wheel a little
        for pos in range(0,360,2):
            show(colors(pos))
            if printFlag:
                print_colors(colors(pos))
        printFlag = False
                
except KeyboardInterrupt:
    clear()
            
