# ws1812_and_led_blink.py: blinks the neopixel and the LED at the same rate
# U. Raich, 17. February 2024
# This program was written for the course on IoT at the University of Cape Coast,Ghana

import neopixel, sys
from utime import sleep_ms
from machine import Pin,Signal

n=1
intensity = 0x1f

print("Testing the ws2812 rgb LED")
print("Blinks the neopixel in blue nad the LED at a frequency of 1 Hz")
print("Program written for the course on IoT at the")
print("University of Cape Coast,Ghana")
print("Copyright: U.Raich")
print("Released under the Gnu Public License")

def clearPixel():
    neoPixel[0] = (0,0,0)
    neoPixel.write()

ws2812 = Pin(33) # connected to GPIO 48 on FreeNove ESP32S3-WROOM
ledPin = Pin(34,Pin.OUT)
led = Signal(ledPin,invert=True)
neoPixel = neopixel.NeoPixel(ws2812, n)

while True:
    try:
        # set the neopixel to green 
        neoPixel[0] = (0,intensity,0);
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
