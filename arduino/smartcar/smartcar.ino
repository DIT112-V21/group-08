#include <MQTT.h>
#include <WiFi.h>
#include <Smartcar.h>

MQTTClient mqtt;

const int lDegrees = -90; // degrees to turn left
const int rDegrees = 90;  // degrees to turn right
int manualSpeed = 70;
bool goingForward = true; //true is forward, false is backward

ArduinoRuntime arduinoRuntime;
BrushedMotor leftMotor(arduinoRuntime, smartcarlib::pins::v2::leftMotorPins);
BrushedMotor rightMotor(arduinoRuntime, smartcarlib::pins::v2::rightMotorPins);
DifferentialControl control(leftMotor, rightMotor);


SimpleCar car(control);

void setup() {
    Serial.begin(9600);
    //Uncomment line below
    //mqtt.begin("localhost", 1883, WiFi);
    // Will connect to localhost port 1883 be default
    if (mqtt.connect("arduino", "public", "public")) {
        mqtt.subscribe("/", 2); // Subscribing to topic "/"
        mqtt.subscribe("speed", 2); //Subscribing to topic "speed"
        mqtt.onMessage(+[](String topic, String message) {
          Serial.println(message);
            if(topic == "/"){
              if(message == "w") {
                car.setSpeed(manualSpeed);
                car.setAngle(0);
                Serial.println("XXX");
              }
              else if(message == "stop") {
                car.setSpeed(0);
                car.setAngle(0);
              }
              else if(message == "s") {
                car.setSpeed(-manualSpeed);
                car.setAngle(0);
              }
              else if(message == "d") {
                car.setSpeed(manualSpeed);
                car.setAngle(rDegrees);
              }
              else if(message == "a") {
                car.setSpeed(manualSpeed);
                car.setAngle(lDegrees);
              }
              else {
                car.setSpeed(0);
                car.setAngle(0);
              }
            }
            if(topic == "speed"){
              car.setSpeed(message.toInt());
              car.setAngle(0);
            }
    }
            
            
        );}
}


// Start server in terminal with: /usr/local/sbin/mosquitto

// Start sketch

// In terminal write: mosquitto_pub -h 127.0.0.1 -t / -m "MESSAGE HERE"
// and it will show up in serial.

// To subscribe in terminal write: mosquitto_sub -h 127.0.0.1 -t /



void loop() {
    if (mqtt.connected()) {
        //mqtt.publish("/", "Hello");
        //mqtt.publish("speed", manualSpeed);
        mqtt.loop();
    }
}
