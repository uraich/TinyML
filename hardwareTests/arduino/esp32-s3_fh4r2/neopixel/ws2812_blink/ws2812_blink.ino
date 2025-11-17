/*
  ws2812_blink: blinks the LED in white
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
  
  // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
  // Here we're using a moderately bright white color:
    
  pixels.setPixelColor(0, pixels.Color(0, 0, RGB_BRIGHTNESS));
  pixels.show();   // Send the updated pixel colors to the hardware.

  delay(DELAY);    // wait for this amount of time with the LEDs on

}
