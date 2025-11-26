# hw_esp32-s3-wrover.py: defines all the hardware connections of the
# esp32-s3_wrover module
# 
# Copyright (c) U. Raich, Mar. 2024
# This file is part of the course on TinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

from micropython import const

# user LED
USER_LED        = const(4) 

# user switch
USER_SWITCH     = const(0)

# flash light
FLASH           = const(4)  # HS2_DATA1
INTENSITY       = const(20) # 20% of max intensity

# pin assignments are:
# The board uses 1 bit SDMMC mode only
# SD card holder  GPIO
# 0   SHELL        GND  
# 1   DAT2          NC
# 2   CD/DAT3       NC     
# 3   CMD           15
# 4   VDD          Vdd
# 5   CLK           14
# 6   VSS          GND        
# 7   DAT0/DO        2
# 8   DAT1/IRQ      NC
# 9   DAT2/NC       NC


MMC_SLOT        = const(0)
MMC_WIDTH       = const(1)
MMC_CLK         = const(39)
MMC_CMD         = const(15)
MMC_D0          = const(2)

# camera
CAM_D0          = const(4)     # Y2 
CAM_D1          = const(5)     # Y3
CAM_D2          = const(18)    # Y4
CAM_D3          = const(19)    # Y5
CAM_D4          = const(36)    # Y5
CAM_D5          = const(39)    # Y7
CAM_D6          = const(34)    # Y7
CAM_D7          = const(35)    # Y9
CAM_HREF        = const(23)
CAM_VSYNC       = const(25)
CAM_RESET       = const(-1)
CAM_PWDN        = const(-1)
CAM_SIOC        = const(27)
CAM_SIOD        = const(26)
CAM_XCLK        = const(21)
CAM_PCLK        = const(22)

