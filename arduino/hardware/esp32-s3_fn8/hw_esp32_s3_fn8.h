/* hw_esp32_s3_fn8.h: defines all the hardware connections of the
   esp32-s3_fn8 CPU
   Copyright (c) U. Raich, Oct. 2025
   This file is part of the course on TinyML at the
   University of Cape Coast, Ghana
   It is released under the MIT license */

// user LED
#define USER_LED        34

// user switch
#define USER_SWITCH     38

// neopixel

#define NEOPIXEL         33
#define NO_OF_NEOPIXELS   1
#define INTENSITY      0x1f

/*
pin assignments are:
SD card holder  SPI   GPIO
1   DAT3/CS      SS    38
2   CMD/DI     MOSI    39
3   VSS1        GND
4   VDD        3.3V
5   CLK/SCK     CLK    42
6   VSS2        GND
7   DAT0/DO    MOSI    41
8   DAT1/IRQ           40
9   DAT2/NC            37
*/

// sd card
#define SD_SLOT         2
#define SD_SS          38
#define SD_MOSI        39
#define SD_SCK         42
#define SD_MISO        41
#define SD_IRQ         40
#define SD_DAT2        37

// camera

#define CAM_D0         5
#define CAM_D1         3
#define CAM_D2         2
#define CAM_D3         4
#define CAM_D4         6
#define CAM_D5         8
#define CAM_D6         9
#define CAM_D7         11
#define CAM_HREF       12
#define CAM_VSYNC      13
#define CAM_RESET      -1
#define CAM_PWDN       -1
#define CAM_SIOC       14
#define CAM_SIOD       21
#define CAM_XCLK       10
#define CAM_PCLK        7

// microphone

#define MIC_WS         37
#define MIC_SCK        36
#define MIC_SD         35

