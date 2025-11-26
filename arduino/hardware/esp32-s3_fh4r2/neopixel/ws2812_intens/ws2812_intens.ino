# ws.ino1812_intens.ino: increases and decreases the light intensity on the
# esp32s3 neopixel
# Copyright (c) U. Raich 25. Oct. 2025
# This program is part of the course on tinyML at the
# University of Cape Coast, Ghana
# It is released under the MIT license

#include <Adafruit_NeoPixel.h>

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals.
// NEO_RGB defines the type of LED
// some LEDs switch red and green
Adafruit_NeoPixel pixels(1, PIN_NEOPIXEL, NEO_RGB + NEO_KHZ800);

void setup() {
  delay(200);   // wait for the esp32-s3_fh4r2 to come up
  Serial.begin(115200);
  Serial.println("Cycles through the light intensity from 10 to 100 and back to 10");
  pixels.begin(); // initialize the  NeoPixel strip object
}

void loop() {
  // increase the light intensity
  for (int i=0;i<100;i++) {
    pixels.setPixelColor(0,pixels.Color(0,0,i));  // change intensity of blue  
    pixels.show();
    delay(20);   
  }

  // decrease the light intensity 
  for (int i=100; i>0;i--) {
    pixels.setPixelColor(0,pixels.Color(0,0,i));  // change intensity of blue  
    pixels.show();
    delay(20); 
  }
}
