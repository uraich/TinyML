/*
  clear_ws2812: switches the LED off
  The wemos esp32s3 board uses a ws2812 neopixel
  Copyright (c) U. Raich 20. Oct. 2025
  This program is part of the course on tinyML at the
  University of Cape Coast, Ghana
  It is released under the MIT license */

#include <Adafruit_NeoPixel.h>

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals.
// NEO_RGB defines the type of LED
// some LEDs switch red and green
Adafruit_NeoPixel pixels(1, PIN_NEOPIXEL, NEO_RGB + NEO_KHZ800);

#define DELAY 500 // Time (in milliseconds) in between colors

void setup() {
  pixels.begin(); // initialize the  NeoPixel strip object
}

void loop() {
  pixels.clear(); // Set all pixel colors to 'off'
  pixels.show();
  delay(DELAY);   // Wait this amount of time with le LEDs off

  for (;;);       // wait forever
}
