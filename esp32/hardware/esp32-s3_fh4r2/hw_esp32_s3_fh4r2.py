# hw_esp32_s3_fh4r2.py: defines all the hardware connections of the
# esp32-s3_fh4r2 CPU
# Copyright (c) U. Raich, Feb. 2024
# This file is part of the course on TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from micropython import const

# neopixel
NEOPIXEL        = const(47)
NO_OF_NEOPIXELS = const(1)
INTENSITY       = const(0x1f)

# user switch
USER_SWITCH     = const(0)

# I2C
SCL             = const(12)
SDA             = const(13)

# microphone
MIC_WS          = const(26)
MIC_SCK         = const(22)
MIC_SD          = const(21)
