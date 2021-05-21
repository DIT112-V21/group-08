#include <MQTT.h>
#include <WiFi.h>
#include <Smartcar.h>
#include <vector>

#ifdef __SMCE__
#include <OV767X.h>
#endif

MQTTClient mqtt;

const int lDegrees = -90; // degrees to turn left
const int rDegrees = 90;  // degrees to turn right
int manualSpeed = 70;
bool goingForward = true; //true is forward, false is backward
const unsigned long LEFT_PULSES_PER_METER  = 600;
const unsigned long RIGHT_PULSES_PER_METER = 740;
const double SPEED_REDUCE = 0.3;
std::vector<char> frameBuffer;

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
    #ifdef __SMCE__
    Camera.begin(VGA, RGB888, 30);
    frameBuffer.resize(Camera.width() * Camera.height() * Camera.bytesPerPixel());
    mqtt.begin("localhost", 1883, WiFi);
    #else
    mqtt.begin(net);
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
            else if(message == "w") {
              waitStop();
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
        const auto currentTime = millis();
    #ifdef __SMCE__
        static auto previousFrame = 0UL;
        if(currentTime - previousFrame >= 65){
          previousFrame = currentTime;
          Camera.readFrame(frameBuffer.data());
          mqtt.publish("/camera", frameBuffer.data(), frameBuffer.size(), false, 0);
        }
    #endif    
    }
    
    #ifdef __SMCE__
    delay(35);
    #endif
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
