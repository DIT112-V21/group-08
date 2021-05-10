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

SmartCar car(arduinoRuntime, control, gyro, leftOdometer, rightOdometer);



// Instructions for starting and using mosquitto on macOS
// Start server with terminal: /usr/local/sbin/mosquitto

// Start sketch

// In terminal write: mosquitto_pub -h 127.0.0.1 -t / -m "MESSAGE HERE"
// and it will show up in serial.

// To subscribe in terminal write: mosquitto_sub -h 127.0.0.1 -t /



void setup() {
    Serial.begin(9600);
    // IMPORTANT: Uncomment line bellow (line 54) before compiling, causes error in CI for some reason but works perfectly fine in SMCE
    //mqtt.begin("localhost", 1883, WiFi);
    // Will connect to localhost port 1883 be default
    if (mqtt.connect("arduino", "public", "public")) {
        mqtt.subscribe("/", 2);    // Subscribing to topic "/"
        mqtt.onMessage(+[](String topic, String message) {
            // handle the message
            Serial.println("Topic: " + topic + " Message: " + message);
            if(message == "r0.0") {
              gyro.update();
              rotateTo0(gyro.getHeading());
            }
            else if(message == "r315.0") {
              gyro.update();
              rotateTo315(gyro.getHeading());
            }
            else if(message == "r270.0") {
              gyro.update();
              rotateTo270(gyro.getHeading());
            }
            else if(message == "r225.0") {
              gyro.update();
              rotateTo225(gyro.getHeading());
            }
            else if(message == "r180.0") {
              gyro.update();
              rotateTo180(gyro.getHeading());
            }
            else if(message == "r135.0") {
              gyro.update();
              rotateTo135(gyro.getHeading());
            }
            else if(message == "r90.0") {
              gyro.update();
              rotateTo90(gyro.getHeading());
            }
            else if(message == "r45.0") {
              gyro.update();
              rotateTo45(gyro.getHeading());
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
        mqtt.publish("/distance", String(rightOdometer.getDistance()));
        gyro.update();
        mqtt.publish("/rotation", String(gyro.getHeading()));
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


void rotateTo0(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    


    int gyroCurrent = startGyro;

    do {
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
    } while(gyroCurrent != 180);
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void rotateTo45(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    


    int gyroCurrent = startGyro;

    do {
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
    } while(gyroCurrent != 135);
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void rotateTo90(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    


    int gyroCurrent = startGyro;

    do {
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
    } while(gyroCurrent != 90);
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void rotateTo135(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    


    int gyroCurrent = startGyro;

    do {
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
    } while(gyroCurrent != 45);
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void rotateTo180(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    


    int gyroCurrent = startGyro;

    do {
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
    } while(gyroCurrent != 0 || gyroCurrent != 360);
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void rotateTo225(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    


    int gyroCurrent = startGyro;

    do {
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
    } while(gyroCurrent != 315);
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void rotateTo270(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    


    int gyroCurrent = startGyro;

    do {
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
    } while(gyroCurrent != 270);
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void rotateTo315(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    


    int gyroCurrent = startGyro;

    do {
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
    } while(gyroCurrent != 225);
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}
