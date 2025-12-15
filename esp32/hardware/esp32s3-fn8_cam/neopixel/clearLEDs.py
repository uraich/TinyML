# clearLEDs: switches off the neopixel and the LED
# U. Raich, 15. April 2025
# This program was written for the course on IoT at the University of Cape Coast,Ghana

import neopixel, sys
from utime import sleep_ms
from machine import Pin,Signal

try:
    from hw_esp32_s3_fn8 import USER_LED, NEOPIXEL, NO_OF_NEOPIXELS, INTENSITY
except:
    print("Please make sure hw_esp32_s3_fn8.py has been uploaded to /lib")
    sys.exit()
    
print("Switching off the ws2812 rgb LED")
print("Program written for the course on IoT at the")
print("University of Cape Coast,Ghana")
print("Copyright: U.Raich")
print("Released under the Gnu Public License")

def clearPixel():
    neoPixel[0] = (0,0,0)
    neoPixel.write()

ws2812 = Pin(NEOPIXEL) # connected to GPIO 33 on ESP32-S3_FN8
ledPin = Pin(USER_LED,Pin.OUT)
led = Signal(ledPin,invert=True)
neoPixel = neopixel.NeoPixel(ws2812, NO_OF_NEOPIXELS)

clearPixel()
led.off()
