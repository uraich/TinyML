# ws1812_and_led_blink.py: blinks the neopixel and the LED at the same rate
# U. Raich, 17. February 2024
# This program was written for the course on IoT at the University of Cape Coast,Ghana

import neopixel, sys
from utime import sleep_ms
from machine import Pin,Signal

try:
    from hw_esp32_s3_wroom import USER_LED, NEOPIXEL, NO_OF_NEOPIXELS, INTENSITY
except:
    print("Please make sure hw_esp32_s3_wroom.py has been uploaded to /lib")
    sys.exit()

print("Testing the ws2812 rgb LED")
print("Blinks the neopixel in green and the user LED at a frequency of 1 Hz")
print("Program written for the course on IoT at the")
print("University of Cape Coast,Ghana")
print("Copyright: U.Raich")
print("Released under the Gnu Public License")

def clearPixel():
    neoPixel[0] = (0,0,0)
    neoPixel.write()

ws2812 = Pin(NEOPIXEL) # connected to GPIO 33 on ESP32-S3_FN8
ledPin = Pin(USER_LED,Pin.OUT)
led = Signal(ledPin,invert=False)
neoPixel = neopixel.NeoPixel(ws2812, NO_OF_NEOPIXELS)

while True:
    try:
        # set the neopixel to green 
        neoPixel[0] = (0,INTENSITY,0);
        neoPixel.write()
        led.on()
        sleep_ms(500)
    
        clearPixel()
        led.off()
        sleep_ms(500)
    except KeyboardInterrupt:
        print("Ctrl C seen! Switching LED off")
        led.off()
        clearPixel()
        sys.exit(0)    
