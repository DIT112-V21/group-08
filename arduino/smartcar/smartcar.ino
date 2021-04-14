#include <MQTT.h>
#include <WiFi.h>

MQTTClient mqtt;

void setup() {
    Serial.begin(9600);
    mqtt.begin("localhost", 1883, WiFi);
    // Will connect to localhost port 1883 be default
    if (mqtt.connect("arduino", "public", "public")) {
        mqtt.subscribe("/", 2); // Subscribing to topic "/"
        mqtt.onMessage(+[](String topic, String message) {
            // handle the message
            Serial.println("Topic: " + topic + " Message: " + message);
        });
    }
}

// Start server in terminal with: /usr/local/sbin/mosquitto

// Start sketch

// In terminal write: mosquitto_pub -h 127.0.0.1 -t / -m "MESSAGE HERE"
// and it will show up in serial.

// To subscribe in terminal write: mosquitto_sub -h 127.0.0.1 -t /


void loop() {
    if (mqtt.connected()) {
        //mqtt.publish("/", "Hello");
        mqtt.loop();
    }
}
