/*
  ws.ino1812_basic_colors: shows all the basic colors on the LED
  The wemos esp32s3 board uses a ws2812 neopixel
  Copyright (c) U. Raich 20. Oct. 2025
  This program is part of the course on tinyML at the
  University of Cape Coast, Ghana
  It is released under the MIT license
*/

#include <Adafruit_NeoPixel.h>

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals.
// NEO_RGB defines the type of LED
// some LEDs switch red and green
Adafruit_NeoPixel pixels(1, PIN_NEOPIXEL, NEO_RGB + NEO_KHZ800);

#define DELAY 2000 // Time (in milliseconds) in between colors

void setup() {
  pixels.begin(); // initialize the  NeoPixel strip object
}

void loop() {
  pixels.clear(); // Set all pixel colors to 'off'
  pixels.show();
  int color,red,green,blue;
  int i;

  for (color=1; color < 8; color++) {
    if (color & 1)
      red = RGB_BRIGHTNESS;
    else
      red = 0;
    
    if (color & 2)
      green = RGB_BRIGHTNESS;
    else
      green = 0;
    
    if (color & 4)
      blue = RGB_BRIGHTNESS;
    else
      blue = 0;
    
    pixels.setPixelColor(0, pixels.Color(red,green,blue));
    pixels.show();

    delay(DELAY);
  }
  // stop the program
  pixels.clear(); // Set all pixel colors to 'off'
  pixels.show();
  for(;;); // stop
}
