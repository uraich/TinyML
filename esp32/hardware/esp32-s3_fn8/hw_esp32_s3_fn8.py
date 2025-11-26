# hw_esp32_s3_f8n.py: defines all the hardware connections of the
# esp32-s3_fn8 CPU
# Copyright (c) U. Raich, Feb. 2024
# This file is part of the course on TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from micropython import const

# user LED
USER_LED        = const(34)

# user switch
USER_SWITCH     = const(38)

# neopixel
NEOPIXEL        = const(33)
NO_OF_NEOPIXELS = const(1)
INTENSITY       = const(0x1f)

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

# sd card
SD_SLOT         = const(2)
SD_SS           = const(38)
SD_MOSI         = const(39)
SD_SCK          = const(42)
SD_MISO         = const(41)
SD_IRQ          = const(40)
SD_DAT2         = const(37)

MMC_SLOT        = const(0)
MMC_WIDTH       = const(1)
MMC_CLK         = const(39)
MMC_CMD         = const(38)
MMC_D0          = const(41)
MMC_D1          = const(40)
MMC_D2          = const(37)
MMC_D3          = const(38)

# camera
CAM_D0          = const(5)
CAM_D1          = const(3)
CAM_D2          = const(2)
CAM_D3          = const(4)
CAM_D4          = const(6)
CAM_D5          = const(8)
CAM_D6          = const(9)
CAM_D7          = const(11)
CAM_HREF        = const(12)
CAM_VSYNC       = const(13)
CAM_RESET       = const(-1)
CAM_PWDN        = const(-1)
CAM_SIOC        = const(14)
CAM_SIOD        = const(21)
CAM_XCLK        = const(10)
CAM_PCLK        = const(7)

# microphone
MIC_WS          = const(37)
MIC_SCK         = const(36)
MIC_SD          = const(35)
