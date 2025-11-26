/*
  magic_wand_ble.ino: Collects all the BlueTooth code from Pete Warden's
  magic_wand.ino program
  connects to the Web server written in JavaScript
  Copyright (c) U. Raich Nov 2025
  This program is part of the TinyML course at the
  University of Cape Coast, Ghana
  It is released under the MIT license
*/
#include "esp_mac.h"
#include <Adafruit_NeoPixel.h>
#include "../../hw_esp32_s3_fh4r2.h"

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLEAddress.h>

Adafruit_NeoPixel pixels(NO_OF_NEOPIXELS, NEOPIXEL, NEO_RGB + NEO_KHZ800);
#define DELAY 500 // Time (in milliseconds) in between colors

#define BLE_SENSE_UUID(val) ("4798e0f2-" val "-4d68-af64-8a8f5258404e")
int connected = false;
int ledOn = false;
namespace {
  
  constexpr int stroke_transmit_stride = 2;
  constexpr int stroke_transmit_max_length = 160;
  constexpr int stroke_max_length = stroke_transmit_max_length * stroke_transmit_stride;
  constexpr int stroke_points_byte_count = 2 * sizeof(int8_t) * stroke_transmit_max_length;
  constexpr int stroke_struct_byte_count = (2 * sizeof(int32_t)) + stroke_points_byte_count;
  
  String serviceUUID = BLE_SENSE_UUID("0000");
  String strokeCharacteristicUUID = BLE_SENSE_UUID("300a");

  // String to calculate the local and device name
  String name;

}; // namespace

class ServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer *pServer) {
    connected=true;
    Serial.print("Client connected");
  };

  void onDisconnect(BLEServer *pServer) {
    connected = false;
    Serial.print("Client disconnected.");
  }
};

void setup() {

  uint8_t mac_address[6] = {0};
  int ret;
  // Need to delay after rebooting the LoLin S3 mini, in order to get full serial output
  delay(200);

  Serial.begin(115200);
  Serial.println("Starting BLE work!");
  Serial.print("stroke_transmit_stride: ");
  Serial.println(stroke_transmit_stride);
  Serial.print("stroke_transmit_max_length: ");
  Serial.println(stroke_transmit_max_length);
  Serial.print("stroke_max_length: ");
  Serial.println(stroke_max_length);
  Serial.print("stroke_points_byte_count: ");
  Serial.println(stroke_points_byte_count);
  Serial.print("stroke_struct_byte_count: ");
  Serial.println(stroke_struct_byte_count);

  Serial.print("WS2812 is connected to GPIO ");
  Serial.println(LED_BUILTIN);
  
  ret = esp_read_mac(mac_address, ESP_MAC_EFUSE_FACTORY);
  if (ret != ESP_OK)
    Serial.println("Could not read MAC address from efuse");
  else
    Serial.println("MAC address read just fine");

  for (int i=0; i<5; i++) {
    Serial.print(mac_address[i],HEX);
    Serial.print(":");
  }
  Serial.println(mac_address[5]+2,HEX); //BlueTooth MAC is the base MAC + 2 on the last octect

  char ch_address[13];
  sprintf(ch_address,"%02x%02x%02x%02x%02x",mac_address[0],mac_address[1],mac_address[2],mac_address[3],mac_address[4],mac_address[5]);
  String address = String(ch_address);
  Serial.print("MAC as string: ");
  Serial.println(address);
  name = "BLESense-";
  name += address[address.length() - 5];
  name += address[address.length() - 4];
  name += address[address.length() - 2];
  name += address[address.length() - 1];
  Serial.print("BLE device name: ");
  Serial.println(name);

  Serial.print("serviceUUID: ");
  Serial.println(serviceUUID);
  Serial.print("strokeCharacteristicUUID: ");
  Serial.println(strokeCharacteristicUUID);

  BLEDevice::init(name);

  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());
  
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
  Serial.println("Waiting for client connections to notify...");
}

void loop() {
  if (connected) {
    pixels.setPixelColor(0, pixels.Color(0, 0, RGB_BRIGHTNESS));
    pixels.show();
    delay(200);
  }
  else {
    if (ledOn) {
      pixels.clear();
      pixels.show();
      ledOn = false;
      delay(200);
    }
    else {  
      pixels.setPixelColor(0, pixels.Color(0, 0, RGB_BRIGHTNESS));
      pixels.show();
      ledOn = true;
      delay(200);
    }
  }

}
