#include <MQTT.h>
#include <WiFi.h>
#include <Smartcar.h>

MQTTClient mqtt;

const int lDegrees = -90; // degrees to turn left
const int rDegrees = 90;  // degrees to turn right
int manualSpeed = 70;
bool goingForward = true; //true is forward, false is backward
const unsigned long LEFT_PULSES_PER_METER  = 600;
const unsigned long RIGHT_PULSES_PER_METER = 740;
const double SPEED_REDUCE = 0.3;

ArduinoRuntime arduinoRuntime;
BrushedMotor leftMotor(arduinoRuntime, smartcarlib::pins::v2::leftMotorPins);
BrushedMotor rightMotor(arduinoRuntime, smartcarlib::pins::v2::rightMotorPins);
DifferentialControl control(leftMotor, rightMotor);

DirectionalOdometer leftOdometer{
    arduinoRuntime,
    smartcarlib::pins::v2::leftOdometerPins,
    []() { leftOdometer.update(); },
    LEFT_PULSES_PER_METER};
DirectionalOdometer rightOdometer{
    arduinoRuntime,
    smartcarlib::pins::v2::rightOdometerPins,
    []() { rightOdometer.update(); },
    RIGHT_PULSES_PER_METER};

const int GYROSCOPE_OFFSET = 37;
GY50 gyro(arduinoRuntime, GYROSCOPE_OFFSET);
#ifndef __SMCE__
WiFiClient net;
#endif

SmartCar car(arduinoRuntime, control, gyro, leftOdometer, rightOdometer);



// Instructions for starting and using mosquitto on macOS
// Start server with terminal: /usr/local/sbin/mosquitto

// Start sketch

// In terminal write: mosquitto_pub -h 127.0.0.1 -t / -m "MESSAGE HERE"
// and it will show up in serial.

// To subscribe in terminal write: mosquitto_sub -h 127.0.0.1 -t /



void setup() {
    Serial.begin(9600);
    // Hopefully this will let us get bast the Arduino_CLI Continuous Integration
    #ifndef __SMCE__
    mqtt.begin(net);
    #else
    mqtt.begin("localhost", 1883, WiFi);
    #endif
    // Will connect to localhost port 1883 be default
    if (mqtt.connect("arduino", "public", "public")) {
        mqtt.subscribe("/", 2);    // Subscribing to topic "/"
        mqtt.onMessage(+[](String topic, String message) {
            // handle the message
            Serial.println("Topic: " + topic + " Message: " + message);
            if(message == "r0.0") {
              gyro.update();
              int roTo = 0;
              rotateTo(gyro.getHeading(), roTo);
            }
            else if(message == "r315.0") {
              gyro.update();
              int roTo = 315;
              rotateTo(gyro.getHeading(), roTo);
            }
            else if(message == "r270.0") {
              gyro.update();
              int roTo = 270;
              rotateTo(gyro.getHeading(), roTo);
            }
            else if(message == "r225.0") {
              gyro.update();
              int roTo = 225;
              rotateTo(gyro.getHeading(), roTo);
            }
            else if(message == "r180.0") {
              gyro.update();
              int roTo = 180;
              rotateTo(gyro.getHeading(), roTo);
            }
            else if(message == "r135.0") {
              gyro.update();
              int roTo = 135;
              rotateTo(gyro.getHeading(), roTo);
            }
            else if(message == "r90.0") {
              gyro.update();
              int roTo = 90;
              rotateTo(gyro.getHeading(), roTo);
            }
            else if(message == "r45.0") {
              gyro.update();
              int roTo = 45;
              rotateTo(gyro.getHeading(), roTo);
            }
            else if(message == "wait") {
              waitStop();
            }
            else if(message == "w"){
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
              goForward(message.toDouble());
            }
            
            
        });
    }
}


void loop() {
    if (mqtt.connected()) { 
        mqtt.loop();
    }
}

void goForward(double distance) {
  double currentDistance;
  double startDistance = car.getDistance();
  do {
    currentDistance = car.getDistance();
    car.setSpeed(manualSpeed);
    car.setAngle(0);
  } while(currentDistance < startDistance + distance);
  car.setSpeed(0);
  car.setAngle(0);
}

void waitStop(){
  car.setSpeed(0);
  rightMotor.setSpeed(0);
  leftMotor.setSpeed(0);


  while(car.getDistance() > 0.010){
    delay(10); 
  }
  
}
//Generalized turning methods into one and made it so it can turn left or right depending on what is quickest 
void rotateTo(int startGyro, int roTo){ 
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    int gyroCurrent = startGyro;
    int checkDistance = (roTo - startGyro);
    int anotherCheck = (360 - abs(checkDistance));  
    Serial.println(startGyro);

    while (gyroCurrent != roTo){
      gyro.update();
      gyroCurrent = car.getHeading();
     if(checkDistance < 0 && abs(checkDistance) <= anotherCheck ){
      rightMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * manualSpeed); 
     }
     else if(checkDistance < 0 && abs(checkDistance) > anotherCheck ){
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed); 
     }
     else if(checkDistance > 0 && abs(checkDistance) <= anotherCheck){
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
     }
     else if(checkDistance > 0 && abs(checkDistance) > anotherCheck){
      rightMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * manualSpeed);
     }
     
    }
    car.setSpeed(0);
}
