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

#include "Arduino.h"
#include "output_handler.h"
#include "tensorflow/lite/micro/micro_log.h"
#include <LiteLED.h>

// The ESP32S3-WROOM uses a neopixel on pin 47
#define LED_TYPE         LED_STRIP_WS2812
#define LED_GPIO         47
#define LED_TYPE_IS_RGBW 0
LiteLED led( LED_TYPE, LED_TYPE_IS_RGBW );

static const crgb_t L_BLUE = 0x0000ff;

// Track whether the function has run at least once
bool initialized = false;

void HandleOutput(float x_value, float y_value) {
    // Do this only once
  if (!initialized) {
    // Set the LED pin to output
    led.begin(LED_GPIO,1);
    led.brightness( 0 );
    led.setPixel(0,L_BLUE,1);
    initialized = true;
  }
    // Calculate the brightness of the LED such that y=-1 is fully off
  // and y=1 is fully on. The LED's brightness can range from 0-255.
  int brightness = (int)(127.5f * (y_value + 1));    // restrict brightness in order not to damage your eyes 

  // The y value is not actually constrained to the range [-1, 1], so we need to
  // clamp the brightness value before sending it to the PWM/LED.
  int brightness_clamped = std::min(255, std::max(0, brightness));

  // this will result in the LED being on when brightness_clamped > 127, off
  // otherwise.
  led.brightness((uint8_t)(brightness_clamped/2), 1);

  // Log the current brightness value for display in the Arduino plotter
  MicroPrintf("%f, %f", static_cast<double>(x_value),
              static_cast<double>(y_value));
  // To print the values to the sceen:
  // MicroPrintf("x_value: %f, y_value: %f", static_cast<double>(x_value),
  //            static_cast<double>(y_value));
  delay(100);
}
