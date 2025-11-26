# hw_esp32_s3_wroom.py: defines all the hardware connections of the
# Freenove esp32_s3_wroom board
# Copyright (c) U. Raich, Feb. 2024
# This file is part of the course on TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from micropython import const

# user LED
USER_LED        = const(2)

# user switch
USER_SWITCH     = const(0)

# neopixel
NEOPIXEL        = const(48)
NO_OF_NEOPIXELS = const(1)
INTENSITY       = const(0x1f)

# pin assignments are:
# SD card works in 1 bit SDMMC mode only

MMC_SLOT        = const(0)
MMC_WIDTH       = const(1)
MMC_CLK         = const(39)
MMC_CMD         = const(38)
MMC_D0          = const(40)

# camera
CAM_D0          = const(11)   # Y2
CAM_D1          = const(9)    # Y3
CAM_D2          = const(8)    # Y4
CAM_D3          = const(10)   # Y5
CAM_D4          = const(12)   # Y6
CAM_D5          = const(18)   # Y7
CAM_D6          = const(17)   # Y8
CAM_D7          = const(16)   # Y9
CAM_HREF        = const(7)
CAM_VSYNC       = const(6)
CAM_RESET       = const(-1)
CAM_PWDN        = const(-1)
CAM_SIOC        = const(5)
CAM_SIOD        = const(4)
CAM_XCLK        = const(15)
CAM_PCLK        = const(13)

