/*
  magic_wand_simul.ino: The program simulates the calls to the lsm6ds3 driver
  that are used by the magic wand program
  Copyright (c) U. Raich, Nov 2025
  This program is part of the course on TinyML
  at the University of Cape Coast, Ghana
  It is released under the MIT license
*/

#include <ESP32S3_LSM6DS3.h>
#include "../../hw_esp32_s3_fh4r2.h"

void setup() {
  Serial.begin(115200);
  while (!Serial);
  if (!IMU.begin()) {
    Serial.println("magic_wand_simul.ino failed to initialize IMU!");

    while (1);
  }
  Serial.println("------------------------------------------------------------------");
  Serial.println("Verifying all IMU calls made by magic_wand.ino on the lsm6ds3");
  Serial.println("------------------------------------------------------------------"); 
  Serial.print("Acceleration data rate: ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.print("Acceleration full scale: +-");
  Serial.print(IMU.accelerationFullScale());
  Serial.println(" g");
  Serial.print("Gyroscope data rate: ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.print("Gyroscope full scale: ");
  Serial.print(IMU.gyroscopeFullScale());
  Serial.println(" dps");
  /* setup the FIFO and check the register settings*/
  IMU.setContinuousMode();
  Serial.print("FIFO water mark: 0x");
  Serial.println(IMU.readWatermark(),HEX);
  Serial.print("FIFO odr (FIFO ): ");
  Serial.print(IMU.fifoODR());
  Serial.println(" Hz");
  Serial.print("Accelerometer decimation factor: ");
  Serial.println(IMU.accelerationDecimation());
  Serial.print("Gyroscope decimation factor: ");
  Serial.println(IMU.gyroscopeDecimation());
  Serial.println("");
  Serial.println("acc_x\tacc_y\tacc_z\tgyro_x\t,gyro_y\tgyro_z");
}

void loop() {

  float acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z;

  while (!IMU.accelerationAvailable())
    delay(10);
  IMU.readAccelerationAndGyroscope(acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z);
  Serial.print(acc_x);
  Serial.print('\t');
  Serial.print(acc_y);
  Serial.print('\t');
  Serial.print(acc_z);
  Serial.print('\t');
  Serial.print(gyro_x);
  Serial.print('\t');
  Serial.print(gyro_y);
  Serial.print('\t');
  Serial.println(gyro_z);

}
