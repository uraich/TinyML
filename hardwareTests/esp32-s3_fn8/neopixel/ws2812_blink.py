# ws1812_blink.py: blinks the neopixel 
# U. Raich, 13. September 2023
# adapted to esp32-s3-fn8: 29.Feb. 2024
# This program was written for the course on IoT at the University of Cape Coast,Ghana
# It is released under the MIT license

import machine, neopixel, time, sys

try:
    from hw_esp32_s3_fn8 import NEOPIXEL, NO_OF_NEOPIXELS, INTENSITY
except:
    print("Please make sure hw_esp32_s3_fn8.py has been uploaded to /lib")
    sys.exit()
    
print("Testing the ws2812 rgb LED")
print("Blinks the neopixel in green at a frequency of 1 Hz")
print("Program written for the course on IoT at the")
print("University of Cape Coast,Ghana")
print("Copyright: U.Raich")
print("Released under the Gnu Public License")

def clearPixel():
    neoPixel[0] = (0,0,0)
    neoPixel.write()

ws2812 = machine.Pin(NEOPIXEL) # connected to GPIO 48 on FreeNove ESP32S3-WROOM

neoPixel = neopixel.NeoPixel(ws2812, NO_OF_NEOPIXELS)

while True:
    try:
        # set the neopixel to green 
        neoPixel[0] = (0,INTENSITY,0);
        neoPixel.write()
        time.sleep_ms(500)
        clearPixel()
        time.sleep_ms(500)
    except KeyboardInterrupt:
        clearPixel()
        sys.exit()
