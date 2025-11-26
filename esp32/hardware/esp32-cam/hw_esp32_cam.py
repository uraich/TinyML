# hw_esp32-cam.py: defines all the hardware connections of the
# tkinter esp32-cam module
# 
# Copyright (c) U. Raich, Mar. 2024
# This file is part of the course on TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from micropython import const

# user LED
USER_LED        = const(33)

# user switch
USER_SWITCH     = const(0)

# flash light
FLASH           = const(4)
INTENSITY       = const(20) # 20% of max intensity

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
SD_CLK          = const(14)
SD_CMD          = const(15)
SD_DATA0        = const(39)
SD_DATA1        = const(4)
SD_DATA2        = const(12)
SD_DATA3        = const(13)

# camera
CAM_D0          = const(5)
CAM_D1          = const(18)
CAM_D2          = const(19)
CAM_D3          = const(21)
CAM_D4          = const(36)
CAM_D5          = const(39)
CAM_D6          = const(34)
CAM_D7          = const(35)
CAM_HREF        = const(23)
CAM_VSYNC       = const(25)
CAM_RESET       = const(-1)
CAM_PWDN        = const(-1)
CAM_SIOC        = const(27)
CAM_SIOD        = const(26)
CAM_XCLK        = const(0)
CAM_PCLK        = const(22)

# microphone
MIC_WS          = const(37)
MIC_SCK         = const(36)
MIC_SD          = const(35)
