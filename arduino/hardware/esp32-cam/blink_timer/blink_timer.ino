/*
  blink_timer.ino: blinks the builtin LED using a timer
  Copyright (c) U. Raich 14.Nov.2025
  This program is part of the course on TinyML at the
  University of Cape Coast, Ghana
  It is released under the MIT license
 */

hw_timer_t *Timer0_Cfg = NULL;

void IRAM_ATTR Timer0_ISR()
{
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    // Serial.println("ISR");
}

void setup()
{
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
    if ((Timer0_Cfg = timerBegin(2000)) == NULL) {        // 2 Hz <> 500ms
        Serial.println("Initialzing time failed");
        while (true) {}
    }
    timerAttachInterrupt(Timer0_Cfg, &Timer0_ISR);        // attach ISR
    timerAlarm(Timer0_Cfg, 1000, true,0);
    timerStart(Timer0_Cfg);
}
void loop()
{
    // Do Nothing!
}
