# pb_state_change.py: Reads and prints the state of the pushbutton every 100 ms
# Signals only state changes
# This is part of the course of small physics experiments at the
# African School of Fundamental Physics 2022
# Copyright (c) U.Raich
# The program is released under the MIT license

import sys
from machine import Pin
from time import sleep_ms
try:
    from hw_esp32_s3_fh4r2 import USER_SWITCH
except:
    print("Please make sure hw_esp32_s3_fh4r2.py has been uploaded to /lib")
    sys.exit()
    
switch = Pin(USER_SWITCH,Pin.IN, Pin.PULL_UP) # program the pin to be input  and
                                              # add the pull up resistor

# a function that prints the state of the push button
def print_state(state):
    if state:
        print("Pushbutton is released")
    else:
        print("Pushbutton is pressed")
        
state = switch.value()
print_state(state)

while True:
    new_state = switch.value()
    if new_state != state:
        state = new_state
        print_state(state)
    sleep_ms(100)
