# ws1812_basic_colors.py: shows all the basic colors on the LED
# U. Raich, 13. September 2023
# This program was written for the course on IoT at the University of Cape Coast,Ghana

import machine, neopixel, time

n=1
intensity = 0x1f

print("Testing the ws2812 rgb LED")
print("Shows the 7 basic color combinations")
print("Program written for the course on IoT at the")
print("University of Cape Coast,Ghana")
print("Copyright: U.Raich")
print("Released under the Gnu Public License")

def clearPixel():
    neoPixel[0] = (0,0,0)
    neoPixel.write()

ws2812 = machine.Pin(33) # connected to GPIO 48 on FreeNove ESP32S3-WROOM

neoPixel = neopixel.NeoPixel(ws2812, n)

for color in range(1,8,1):
    if color & 1:
        red = intensity
    else:
        red = 0
        
    if color & 2:
        green = intensity
    else:
        green = 0
        
    if color & 4:
        blue = intensity
    else:
        blue = 0
        
    neoPixel[0] = (red,green,blue)
    neoPixel.write()
    time.sleep(2)
    
clearPixel()

