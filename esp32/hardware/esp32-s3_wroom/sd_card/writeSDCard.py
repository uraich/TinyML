# writeSDCard.py: write a text file to the SD card
# The user programmable LED is connected to GPIO 2
# Copyright (c) U. Raich, Feb, 2024
# This program is part of a course on tinyML for the
# African Internet Summit 2024
# It is released under the MIT license

from time import sleep_ms
from machine import SDCard,Pin,SPI
import os

# create an SD card object
# pin assignments are:
# SD card holder  SPI   GPIO
# 1   DAT3/CS      SS    38
# 2   CMD/DI     MOSI    39
# 3   VSS1        GND
# 4   VDD        3.3V
# 5   CLK/SCK     CLK    42
# 6   VSS2        GND
# 7   DAT0/DO    MOSI    41
# 8   DAT1/IRQ           40
# 9   DAT2/NC            37

#sd_card = SDCard(sck=Pin(42),miso=Pin(41),mosi=Pin(39),cs=Pin(38))
sd_card = SDCard(slot=2,sck=42,miso=41,mosi=39,cs=38)
# mount the sd card
vfs = os.VfsFat(sd_card)
os.mount(vfs,"/sd")

# open a text file for writing
filename = "/sd/helloWorld.txt"
f = open(filename,"w")
f.write("Hello World!\n")
f.close()


