# blink.py: blink the user LED on the esp32-s3fh4r2
# The wemos esp32s3 board uses a ws2812 neopixel
# Copyright (c) U. Raich 11. Oct. 2023
# This program is part of the course on tinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms

LED_PIN    = 47
NO_OF_LEDS = 1
INTENSITY  = 0x1f
ON         = 1
OFF        = 0

led = NeoPixel(Pin(LED_PIN),NO_OF_LEDS)

def switchLED(onOff):
    if onOff:
        led[0] = (INTENSITY,INTENSITY,INTENSITY)
    else:
        led[0]  = (0,0,0)
    led.write()

def led_on():
    switchLED(ON)

def led_off():
    switchLED(OFF)

try:
    while True:
        led_on()
        sleep_ms(500)
        led_off()
        sleep_ms(500)
except KeyboardInterrupt:
    led_off()
