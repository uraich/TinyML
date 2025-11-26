# listSDCard.py: lists all the files on the root folder of the sd card
# The user programmable LED is connected to GPIO 2
# Copyright (c) U. Raich, Feb, 2024
# This program is part of a course on tinyML for the
# African Internet Summit 2024
# It is released under the MIT license

from time import sleep_ms
from machine import SDCard,Pin,SPI
import os

try:
    from hw_esp32_s3_wroom import *
except:
    print("Please make sure hw_esp32_s3_wroom.py has been uploaded to /lib")
    sys.exit()


#sd_card = SDCard(sck=Pin(42),miso=Pin(41),mosi=Pin(39),cs=Pin(38))
sd_card = SDCard(slot  = MMC_SLOT,
                 width = MMC_WIDTH,
                 sck   = MMC_CLK,
                 cmd   = MMC_CMD,
                 data  = [MMC_D0])

# mount the sd card
vfs = os.VfsFat(sd_card)
os.mount(vfs,"/sd")

# list the files in the current directory
files = os.listdir("/sd")
print("files : ")
print(files)


