# pb_state.py: reads the user switch (SW1), which is connected to GPIO 38
# Copyright (c) U. Raich, Feb, 2024
# This program is part of a course on tinyML for the
# African Internet Summit 2024
# It is released under the MIT license

from time import sleep_ms
from machine import Pin,Signal
try:
    from hw_esp32_s3_wroom import USER_SWITCH
except:
    print("Please make sure hw_esp32_s3_wroom.py has been uploaded to /lib")
    sys.exit()

switch = Pin(USER_SWITCH, Pin.IN, Pin.PULL_UP)  

while True:
    if (switch.value()):  # if we get a one here, we see the pullup resistor
                          # this means that the switch is open
        print("Push button is released")
    else:                 # if we read zero, the switch is grounded
                          # this means it must be pressed
        print("Push button is pressed") 
    sleep_ms(100)




