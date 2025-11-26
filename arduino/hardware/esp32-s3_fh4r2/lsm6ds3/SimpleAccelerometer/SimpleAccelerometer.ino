/*
  Arduino LSM6DS3 - Simple Accelerometer

  This example reads the accelerometer values from the LSM6DS3
  sensor and continuously prints them to the Serial Monitor
  or Serial Plotter.
  The LSM6DS3 FIFO is not used

  created 6. Nov. 2025
  by Uli Raich

  This example code is part of the TinyML course at the
  University of Cape Coast, Ghana
  It is released under the MIT license
*/
#include "../../hw_esp32_s3_fh4r2.h"
#include <ESP32S3_LSM6DS3.h>

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Accelerometer in g's");
  Serial.println("X\tY\tZ");
}

void loop() {
  float x, y, z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    Serial.print(x);
    Serial.print('\t');
    Serial.print(y);
    Serial.print('\t');
    Serial.println(z);
  }
}
