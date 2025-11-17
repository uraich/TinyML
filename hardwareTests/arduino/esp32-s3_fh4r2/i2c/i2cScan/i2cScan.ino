/****************************************************************
  i2c_scan: scans he I2C bus for connected devices
  Uli Raich
  4. October 2025
  This program is part of the TinyML course for the University of
  Cape Coast, Ghana
  It is released under he MIT license
*****************************************************************/

#include <Wire.h>

#define SCL 12 // on the wemos d1 mini (esp32s3fh4r2) scl is connected to GPIO 12
#define SDA 13 // on the wemos d1 mini (esp32s3fh4r2) sda is connected to GPIO 13

void setup() {
  Wire.begin(SDA,SCL);
  Serial.begin(115200);                  // Make sure that Tools -> USB CDC On Boot is enabled
                                         // Otherwise serial output may not work on the ESP32S3 mini board
  while (!Serial && (millis() < 5000));  // Wait up to 5 secs for Serial to be ready
  if (!Serial) {
    for (;;) {} // failed, loop forever
  }
  Serial.println("I2C scan running on the ESP32 Arduino SDK");
  Serial.println("This is a special version for the ESP32S3FH4R2");
  Serial.println("Here SCL : D5 == GPIO 12, SDA: D6 == GPIO 13");
  Serial.println("Program written for the workshop on IoT at the");
  Serial.println("African Internet Summit 2026");
  Serial.println("Copyright: U.Raich");
  Serial.println("Released under the MIT License\n");

  Serial.println("     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f");
}
 
void loop() {
  byte error, i,j;
  //Serial.println("Scanning...");
  char buf[4];
  for(i=0;i<8;i++) {
    sprintf(buf,"%02x: ",i);
    Serial.print(buf);
    buf[3] = '\0';        // use only 3 chracters from now on	    
    for (j=0;j<16;j++) {
      Wire.beginTransmission(16*i+j);
      error = Wire.endTransmission();
      if (error == 0) {
	if (16*i+j<16) {
	  Serial.print("00 ");
	}
	else {
	  sprintf(buf,"%02x ",16*i+j);
	  Serial.print(buf);
	}
      }
      else
	Serial.print("-- ");
    }
    Serial.println();
  }
  for (;;){}; 
}
