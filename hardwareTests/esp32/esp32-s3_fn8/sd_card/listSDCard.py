# listSDCard.py: lists all the files on the root folder of the sd card
# The user programmable LED is connected to GPIO 2
# Copyright (c) U. Raich, Feb, 2024
# This program is part of a course on tinyML for the
# African Internet Summit 2024
# It is released under the MIT license

from time import sleep_ms
from machine import SDCard,Pin,SPI
import os,sys

try:
    from hw_esp32_s3_fn8 import *
except:
    print("Please make sure hw_esp32_s3_fn8.py has been uploaded to /lib")
    sys.exit()

# create an SD card object
sd_card = SDCard(slot=SD_SLOT,sck=SD_SCK,miso=SD_MISO,mosi=SD_MOSI,cs=SD_SS)
# mount the sd card
vfs = os.VfsFat(sd_card)
os.mount(vfs,"/sd")

# list the files in the current directory
files = os.listdir("/sd")
print("files : ")
print(files)


