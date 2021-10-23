// Including the WiFi header
#include <ESP8266WiFi.h>

const char* ssid     = "SSID";     // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "PASSWORD"; // The password for the Wi-Fi network

void setup() {
    Serial.begin(9600); // Start serial
    delay(10);
    Serial.println('\n');

    // Connect to the network
    WiFi.begin(ssid, password);
    Serial.print("Connecting to ");
    Serial.print(ssid); Serial.println(" ...");

    // Wait for the WiFi to connect
    int i = 0;
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(++i); Serial.print(' ');
    }

    Serial.println('\n');
    Serial.println("Connection established!");  
    Serial.print("IP address:\t");
    Serial.println(WiFi.localIP());         // Send the IP address of the ESP8266 to the computer
}

void loop() { }
