# ws2812_blink_timer.py: blink the user LED on the esp32-s3fh4r2
# The wemos esp32s3 board uses a ws2812 neopixel
# Here we use a timer to define the blink frequency
# Copyright (c) U. Raich 14. Nov. 2025
# This program is part of the course on tinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from machine import Pin, Timer
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

led = NeoPixel(Pin(NEOPIXEL),NO_OF_NEOPIXELS)

class NeoPixelLED():
    def __init__(self):
        self.state = False        
        self.led = NeoPixel(Pin(NEOPIXEL),NO_OF_NEOPIXELS)

    def off(self):
        # switch LED off
        self.led[0] = (0,0,0)
        self.led.write()
        self.state = False

    def on(self):
        # switch LED on (blue color)
        self.led[0] = (0,0,INTENSITY)
        self.led.write()
        self.state = True

    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()
            
    def state(self):
        return self.state

ws2812LED = NeoPixelLED()

# Callback function for the timer
def toggle_led(timer):
    ws2812LED.toggle()  # Toggle the LED state (ON/OFF)

# Create a periodic timer
blink_timer = Timer(1)

# Timer repeats every half second
blink_timer.init(mode=Timer.PERIODIC, period=500, callback=toggle_led)

try:
    # Main loop (optional)
    while True:
        # print('Main Loop is running')
        sleep_ms(20000)
except KeyboardInterrupt:
    # Keyboard interrupt occurred, deinitialize the timer
    blink_timer.deinit()
    print('Timer deinitialized')
    # Turn off the LED
    ws2812LED.off()
