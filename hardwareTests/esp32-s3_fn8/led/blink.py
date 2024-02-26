# blink.py: blinks the user LED at 1 Hz
# The user programmable LED is connected to GPIO 2
# Copyright (c) U. Raich, Feb, 2024
# This program is part of a course on tinyML for the
# African Internet Summit 2024
# It is released under the MIT license

from time import sleep_ms
from machine import Pin,Signal
ledPin = Pin(34,Pin.OUT)  #create LED object from pin2,Set Pin2 to output
led=Signal(ledPin,invert=True) 

try:
    while True:
        led.on()            #Set led turn on
        sleep_ms(500)
        led.off()           #Set led turn off
        sleep_ms(500)
except:
    pass





