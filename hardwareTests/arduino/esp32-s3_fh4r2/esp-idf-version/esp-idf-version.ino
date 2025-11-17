/*
  Getting the ESP-IDF version used on the Arduino SDK
*/

void setup() {
  // needed on LoLin 3 mini to get all serial output from the beginning
  // otherwise the first few lines are not seen
  delay(1000);
  Serial.begin(115200);
  while (!Serial)
    delay(10);

  Serial.println("Using ESP object:");
  Serial.println(ESP.getSdkVersion());

  Serial.println("Using lower level function:");
  Serial.println(esp_get_idf_version());
}

void loop() {}
