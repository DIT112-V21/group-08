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
    mqtt.begin("localhost", 1883, WiFi);
    // Will connect to localhost port 1883 be default
    if (mqtt.connect("arduino", "public", "public")) {
        mqtt.subscribe("/", 2); // Subscribing to topic "/"
        mqtt.onMessage(+[](String topic, String message) {
          handleInput(message);
          }
      );
    }
}


void handleInput(String message){

    if(message == "w") {
      car.setSpeed(manualSpeed);
      car.setAngle(0);
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
    else if(message == "q") {
      if ((manualSpeed - 10) >= 0) { // to stop the car from reversing when decrasing speed
                manualSpeed = manualSpeed - 10;
                Serial.println(manualSpeed);
                if (goingForward) {
                  car.setSpeed(manualSpeed);
                } else {
                  car.setSpeed(-manualSpeed);
                }
            }
    }
    else if(message == "e") {
        if ((manualSpeed + 10) <= 100) { // car can't go faster than 100
                manualSpeed = manualSpeed + 10;
                Serial.println(manualSpeed);
                if (goingForward) {
                  car.setSpeed(manualSpeed);
                } else {
                  car.setSpeed(-manualSpeed);
                }
            }
        
    }
    
    
    else {
      car.setSpeed(0);
      car.setAngle(0);
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
