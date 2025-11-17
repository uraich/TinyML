/*
  Trying the use the standard blink program on the ws2812
*/

void setup() {
  delay(200);
  Serial.begin(115200);
  Serial.print("Using digitalWrite to blink the ws2812 LED");

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);  // turn the LED off (LOW is the voltage level)
  delay(500);
}
