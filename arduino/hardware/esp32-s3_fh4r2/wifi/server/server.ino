/* server.ino: Sends some dummy data to a client on the PC for plotting
  The program is used to simulate the transfer of strokes from the magic wand 
  TinyML example and its plotting
  Copyright (c) U. Raich 24.11.2025
  The program is part of the TinyML course at the
  University of Cape Coast, Ghana
  It is released under the MIT license
*/

#include <WiFi.h>
#include <math.h>

const char* ssid = "WLAN18074253";
const char* password = "Q4k6V35sFauw";

#define NO_OF_POINTS 100    // define 100 circle points
float radius = 2.0;
float x[NO_OF_POINTS+1];
float y[NO_OF_POINTS+1];

#define TCP_PORT 5000
WiFiServer tcpServer(TCP_PORT);  // communicate on port 5000
IPAddress localIP;

void setup() {
 delay(200);                    // wait for the ESP32-S3 tocome up
  /* 
    calculate the points of a circle with:
    x = radius*cos(phi])
    y = radius*sin(phi)
  */
  for (int i=0;i<NO_OF_POINTS+1;i++) {           // need an additional point to close the circle
    x[i] = radius*cos(2*M_PI*i/NO_OF_POINTS);
    y[i] = radius*sin(2*M_PI*i/NO_OF_POINTS);   
  }
  
  Serial.begin(115200);
  Serial.println("TCP server demo program");

  for (int i=0;i<10;i++) {
    Serial.print("x: ");
    Serial.print(x[i]);
    Serial.print(", y: ");
    Serial.println(y[i]);
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }
  Serial.println("");
  Serial.print("Connected to WiFi ");
  Serial.println(WiFi.SSID());
  localIP = WiFi.localIP();
  Serial.println("Local IP address: " + localIP.toString());
  //Serial.println(localIP);
  tcpServer.begin();
  Serial.print("TCP server started on port ");
  Serial.println(TCP_PORT);


}

void loop() {
  WiFiClient client = tcpServer.available(); // Check for incoming clients

  if (client) {
    Serial.println("Client connected!");
    Serial.println("Sending greeting message");
    client.println("Connected to " + localIP.toString());
    // wait until the "ok" from the client
    if (client.available()) {
      String data = client.readStringUntil('\n');
      Serial.print("Received: ");
      Serial.println(data);
      if (data != "ok")
        Serial.println("Not ok");
    }
    // send the points
    for (int i=0;i<NO_OF_POINTS+1;i++) {
      String message = String(x[i]) + ", " + String(y[i]);
      Serial.print("message: ");
      Serial.println(message);
      client.println(message);
      // wait for the answer 
      while (!client.available()) ;
      //  Serial.println("Waiting for client");
      String data = client.readStringUntil('\n');
      /*
      Serial.print("Received: ");
      Serial.println(data);
      if (data != "ok") {
        Serial.println("Not ok");
        break;
      } 
      */
    }

    Serial.println("Send end message");
    client.println("bye");
    client.stop();
    Serial.println("Client disconnected.");
  }
}
