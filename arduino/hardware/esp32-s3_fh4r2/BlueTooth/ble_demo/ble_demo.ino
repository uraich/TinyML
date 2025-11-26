/*
  ble_demo.ino: Demonstrates BlueTooth Low Energy on the esp32
  It uses a serial terminal to read and write devices on the esp32-s3_fh4r2
  Copyright (c) U. Raich Nov 2025
  This program is part of the TinyML course at the
  University of Cape Coast, Ghana
  It is released under the MIT license
*/

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLEAddress.h>

# Nordic UART Service (NUS)
#define _NUS_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"

void setup() {

  Serial.begin(115200);
  Serial.println("Starting BLE demo!");

  BLEDevice::init("BLE demo");

  BLEServer *pServer = BLEDevice::createServer();
  BLEService *pService = pServer->createService(serviceUUID);
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
                                         strokeCharacteristicUUID,
                                         BLECharacteristic::PROPERTY_READ 
                                       );

  pCharacteristic->setValue("Hello World says Neil");
  pService->start();
  // BLEAdvertising *pAdvertising = pServer->getAdvertising();  // this still is working for backward compatibility
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(serviceUUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // functions that help with iPhone connections issue
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
  Serial.println("Characteristic defined! Now you can read it in your phone!");

}

void loop() {
  
}
