/*
  ws2812_blink_time: blinks the LED in blue using an esp32 timer with interrupts
  The wemos esp32s3 board uses a ws2812 neopixel
  Copyright (c) U. Raich 17. Nov. 2025
  This program is part of the course on tinyML at the
  University of Cape Coast, Ghana
  It is released under the MIT license */

#include <Adafruit_NeoPixel.h>
#include "esp_task_wdt.h"

hw_timer_t *Timer0_Cfg = NULL;
int ledIsOn = false;
int oldLedIsOn = false;
// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals.
// NEO_RGB defines the type of LED
// some LEDs switch red and green
Adafruit_NeoPixel pixels(1, PIN_NEOPIXEL, NEO_RGB + NEO_KHZ800);

void IRAM_ATTR Timer0_ISR()
{
  // putting pixels.show() into the ISR crashes the code
  if (ledIsOn) {
    ledIsOn = false;
    // Serial.println("off");
  }
  else {
    ledIsOn = true;
    //Serial.println("on");
  }
}

void setup() {
  Serial.begin(115200);
  pixels.begin(); // initialize the  NeoPixel strip object

  pixels.clear();
  pixels.show();
  
  // Initialize the timer to interrupt every 100 ms
  if ((Timer0_Cfg = timerBegin(10000)) == NULL) {       // 10 kHz
    Serial.println("Initialzing time failed");
    while (true) {}
  }
  timerAttachInterrupt(Timer0_Cfg, &Timer0_ISR);        // attach ISR
  timerAlarm(Timer0_Cfg, 1000, true,0);                 // trigger alarm after 1000 ticks
  timerStart(Timer0_Cfg);
  }

void loop() {
  if (oldLedIsOn != ledIsOn) {
    oldLedIsOn = ledIsOn;
    if (ledIsOn) {
      pixels.setPixelColor(0, pixels.Color(0, 0, RGB_BRIGHTNESS));
      pixels.show(); 
    }
    else {
      pixels.clear();
      pixels.show();
    }
  }
}
