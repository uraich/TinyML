/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include "output_handler.h"
#include "constants.h"
#include "tensorflow/lite/micro/micro_log.h"
#include <Adafruit_NeoPixel.h>

extern int maxIntensity;
extern Adafruit_NeoPixel pixels;

void HandleOutput(float x_value, float y_value) {
  // Log the current X and Y values
  MicroPrintf("x_value: %f, y_value: %f", static_cast<double>(x_value),
              static_cast<double>(y_value));
  // calculate the intensity value from the y value of the sine function
  int intens = ((y_value+1)/2)*maxIntensity;
  // The y value might fall below -1 in which case the intensity value
  // would become negative, resulting in a flash of the LED
  if (intens < 0)
    intens = 0;
  pixels.setPixelColor(0,pixels.Color(0,0,intens));  // change intensity of blue
  pixels.show();
}
