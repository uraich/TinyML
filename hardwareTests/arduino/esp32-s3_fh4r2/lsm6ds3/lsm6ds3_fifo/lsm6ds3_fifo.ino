/*
  lsm6ds3_fifo.ino: reads the accelerometer and the gyroscope via the fifo
  This is the C++ version of lsm6ds3_fifo.py
  Copyright (c) U. Raich, Oct 2025
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
    Serial.println("lsm6ds3_fifo.ino failed to initialize IMU!");

    while (1);
  }
  Serial.print("Device ID: 0x");
  Serial.println(IMU.whoAmI(),HEX);

  Serial.println("Reset the device");
  IMU.reset();
  delay(2);
 
  Serial.println("---------------------------------------------------------");
  Serial.println("Setting up the accelerometer");
  Serial.println("output data rate: 104 Hz, full scale: 4g"); 
  Serial.println("---------------------------------------------------------");

  IMU.write_ctrl1_xl(0x4b);
  Serial.print("ctrl1_xl: 0x");
  Serial.println(IMU.read_ctrl1_xl(),HEX);

  Serial.println("---------------------------------------------------------");
  Serial.println("Setting up the gyroscope");
  Serial.println("output data rate: 104 Hz, full scale: 2000 dps"); 
  Serial.println("---------------------------------------------------------\n");

  IMU.write_ctrl2_g(0x4c);
  Serial.print("ctrl2_g: 0x");
  Serial.println(IMU.read_ctrl2_g(),HEX);
  Serial.println("---------------------------------------------------------");
  Serial.println("Set watermark threshold");
  Serial.println("---------------------------------------------------------");
  IMU.writeWatermark(0x200);
  Serial.print("Fifo threshold set to 0x");
  Serial.println(IMU.readWatermark(),HEX);
  Serial.println("Set fifo odr");
  Serial.println("Fifo odr is set to 104 Hz");
  Serial.println("Set the acc and gyro decimation factor to no decimation (factor = 1)");
  IMU.writeFIFO_ctrl3(0x09);
  Serial.print("fifo_ctrl3: 0x");
  Serial.println(IMU.readFIFO_ctrl3(),HEX);
  Serial.println("Set FIFO to continuous mode");
  IMU.writeFIFO_ctrl5(0x26);
  Serial.print("fifo_ctrl5: 0x");
  Serial.println(IMU.readFIFO_ctrl5(),HEX);
  Serial.println("");
  Serial.println("---------------------------------------------------------");
  Serial.println("Read FIFO");
  Serial.println("---------------------------------------------------------");
  Serial.println();
  Serial.println("acc_x\tacc_y\tacc_z\tgyro_x\tgyro_y\tgyro_z");
}

void loop() {
  int data_count;
  int gyro_x_raw, gyro_y_raw, gyro_z_raw;
  int acc_x_raw, acc_y_raw, acc_z_raw;
  float gyro_x, gyro_y, gyro_z;
  float acc_x, acc_y, acc_z;
  while (IMU.fifoIsEmpty())
    delay(10);
  data_count = IMU.wordsInFIFO();
  // Serial.print("values in fifo: ");
  // Serial.println(data_count);
  if (data_count %6)
    Serial.println("wrong data in FIFO");
  else {
    /*
    gyro_x_raw = IMU.fifo_data();
    gyro_y_raw = IMU.fifo_data();
    gyro_z_raw = IMU.fifo_data();
    acc_x_raw = IMU.fifo_data();
    acc_y_raw = IMU.fifo_data();
    acc_z_raw = IMU.fifo_data();
    Serial.println("Data read from FIFO");
    Serial.print(gyro_x_raw);
    Serial.print(", ");
    Serial.print(gyro_y_raw);
    Serial.print(", ");
    Serial.print(gyro_z_raw);
    Serial.print(", ");
    Serial.print(acc_x_raw);
    Serial.print(", ");    
    Serial.print(acc_x_raw);
    Serial.print(", ");
    Serial.print(acc_y_raw);
    Serial.print(", ");
    Serial.println(acc_z_raw);
    */
    gyro_x = IMU.fifo_data() * 2000.0 / 32768.0;
    gyro_y = IMU.fifo_data() * 2000.0 / 32768.0;
    gyro_z = IMU.fifo_data() * 2000.0 / 32768.0;
    acc_x = IMU.fifo_data() * 4.0 / 32768.0;
    acc_y = IMU.fifo_data() * 4.0 / 32768.0;
    acc_z = IMU.fifo_data() * 4.0 / 32768.0;
    // Serial.println("Data read from FIFO");
  
    Serial.print(acc_x);
    Serial.print("\t");    
    Serial.print(acc_y);
    Serial.print("\t");
    Serial.print(acc_z);
    Serial.print("\t");
    Serial.print(gyro_x);
    Serial.print("\t");
    Serial.print(gyro_y);
    Serial.print("\t");
    Serial.println(gyro_z);
  }

}
