# ws1812_blink.py: blinks the neopixel 
# U. Raich, 13. September 2023
# This program was written for the course on IoT at the University of Cape Coast,Ghana

import machine, neopixel, time, sys

n=1
intensity = 0x1f

print("Testing the ws2812 rgb LED")
print("Blinks the neopixel in blue at a frequency of 1 Hz")
print("Program written for the course on IoT at the")
print("University of Cape Coast,Ghana")
print("Copyright: U.Raich")
print("Released under the Gnu Public License")

def clearPixel():
    neoPixel[0] = (0,0,0)
    neoPixel.write()

ws2812 = machine.Pin(33) # connected to GPIO 48 on FreeNove ESP32S3-WROOM

neoPixel = neopixel.NeoPixel(ws2812, n)

while True:
    try:
        # set the neopixel to green 
        neoPixel[0] = (0,intensity,0);
        neoPixel.write()
        time.sleep_ms(500)
        clearPixel()
        time.sleep_ms(500)
    except KeyboardInterrupt:
        clearPixel()
        sys.exit()
