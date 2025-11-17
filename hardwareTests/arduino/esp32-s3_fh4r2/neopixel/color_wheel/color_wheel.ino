/*
  colorwheel:  Shows all the colors of the rainbow on the NeoPixel LEDs
  The wemos esp32s3 board uses a ws2812 neopixel
  Copyright (c) U. Raich 20. Oct. 2025
  This program is part of the course on tinyML at the
  University of Cape Coast, Ghana
  It is released under the MIT license */

#include <Adafruit_NeoPixel.h>
#define MAX_INTENSITY RGB_BRIGHTNESS

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals.
// NEO_RGB defines the type of LED
// some LEDs switch red and green

Adafruit_NeoPixel pixels(1, PIN_NEOPIXEL, NEO_RGB + NEO_KHZ800);

#define DELAY 100 // Time (in milliseconds) in between colors
#define RED   0
#define GREEN 1
#define BLUE  2

void setup() {
  pixels.begin(); // initialize the  NeoPixel strip object
}

int *colors(int pos) {
  static int color_buf[3];
  int red,green,blue;

  if (pos<60) {
    red=MAX_INTENSITY;
    green=(int)(MAX_INTENSITY*pos/60);
    blue=0;
  }
  else if ((pos >=60) && (pos < 120)) {
    red=MAX_INTENSITY-(int)(MAX_INTENSITY*(pos-60)/60);
    green = MAX_INTENSITY;
    blue = 0;
  }
  else if ((pos >=120) && (pos < 180)) {
    red = 0;
    blue = (int)(MAX_INTENSITY*(pos-120)/60);
    green = MAX_INTENSITY;
  }
  else if ((pos >= 180) && (pos < 240)) {
    red = 0;
    green = MAX_INTENSITY-(int)(MAX_INTENSITY*(pos-180)/60);
    blue = MAX_INTENSITY;
  }
  else if ((pos >= 240) && (pos < 300)) {
    red = (int)(MAX_INTENSITY*(pos-240)/60);
    green = 0;
    blue = MAX_INTENSITY;
  }
  else{
    red = MAX_INTENSITY;
    green = 0;
    blue = MAX_INTENSITY - (int)(MAX_INTENSITY*(pos-300)/60);
  }
  color_buf[RED]   =  red;
  color_buf[GREEN] = green;
  color_buf[BLUE]  =  blue;
  return color_buf;
}

void show_color(int *color_buf) {
  pixels.setPixelColor(0, pixels.Color(color_buf[RED], color_buf[GREEN], color_buf[BLUE]));
  pixels.show();   // Send the updated pixel colors to the hardware.
  delay(DELAY);
}
void print_colors(int red, int green, int blue){
  char buf[100];
  sprintf(buf, "red: %03d, green: %03d, blue: %03d",red,green,blue);
  Serial.println(buf);
}

void loop() {
  /*
  if you observe the color wheel very attentively then you see that there is only one color component that
  is changing as we go around the ring.
  0°..60°:     red is constantly at max, blue is constantly zero and green increases
  60°.. 120°:  green is constantly at max, blue is zero and red decreases
  similar for all the 6 sectors
  We must therefore check in which sector the angular position is falling, then we can easily calculate
  the color components depending on the angular position around the ring */
  
  pixels.clear(); // Set all pixel colors to 'off'
  pixels.show();
  delay(DELAY);   // Wait this amount of time with le LEDs off
  int pos;

  // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
  // Here we're using a moderately bright white color:
  for (pos=0; pos<360;pos+=2) {
    show_color(colors(pos));
  }
}
