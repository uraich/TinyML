/*
  print the pin definition from the board specificattion
  Copyright (c) U. Raich 17.11.2025
*/

void setup() {
  delay(200);           // needed on LoLin S3 mini to see all serial output
  Serial.begin(115200);

  Serial.println("The pin definitions from pin pins_arduino.h");
  Serial.print("SOC_GPIO_PIN_COUNT: ");
  Serial.println(SOC_GPIO_PIN_COUNT);
  Serial.print("PIN_NEOPIXEL: ");
  Serial.println(PIN_NEOPIXEL);
  Serial.print("LED_BUILTIN: ");
  Serial.println(LED_BUILTIN);
  Serial.println("I2C specs: ");
  Serial.print("SDA: ");
  Serial.println(SDA);
  Serial.print("SCL: ");
  Serial.println(SCL);

  Serial.println("spi specs:");
  Serial.print("SS: ");
  Serial.println(SS);
  Serial.print("MOSI: ");
  Serial.println(MOSI);
  Serial.print("MISO: ");
  Serial.println(MISO);
  Serial.print("SCK: ");
  Serial.println(SCK);
  
  
}

void loop() {}
