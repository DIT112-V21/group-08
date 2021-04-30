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

ArduinoRuntime arduinoRuntime;
BrushedMotor leftMotor(arduinoRuntime, smartcarlib::pins::v2::leftMotorPins);
BrushedMotor rightMotor(arduinoRuntime, smartcarlib::pins::v2::rightMotorPins);
DifferentialControl control(leftMotor, rightMotor);

DirectionalOdometer leftOdometer(
    arduinoRuntime,
    smartcarlib::pins::v2::leftOdometerPins,
    []() { leftOdometer.update(); },
    LEFT_PULSES_PER_METER);
DirectionalOdometer rightOdometer(
    arduinoRuntime,
    smartcarlib::pins::v2::rightOdometerPins,
    []() { rightOdometer.update(); },
    RIGHT_PULSES_PER_METER);

const int GYROSCOPE_OFFSET = 37;
GY50 gyro(arduinoRuntime, GYROSCOPE_OFFSET);

SimpleCar car(control);





void setup() {
    Serial.begin(9600);
    mqtt.begin("localhost", 1883, WiFi);
    // Will connect to localhost port 1883 be default
    if (mqtt.connect("arduino", "public", "public")) {
        mqtt.subscribe("/", 2);    // Subscribing to topic "/"
        mqtt.onMessage(+[](String topic, String message) {
            // handle the message
            Serial.println("Topic: " + topic + " Message: " + message);
            if(message == "f") {
              car.setSpeed(manualSpeed);
              car.setAngle(0);
            }
            else if(message == "s") {
              car.setSpeed(0);
              car.setAngle(0);
            }
            else if(message == "b") {
              car.setSpeed(-manualSpeed);
              car.setAngle(0);
            }
            else if(message == "r") {
              car.setSpeed(manualSpeed);
              car.setAngle(rDegrees);
            }
            else if(message == "l") {
              car.setSpeed(manualSpeed);
              car.setAngle(lDegrees);
            }
            else if(message == "l") {
              car.setSpeed(manualSpeed);
              car.setAngle(lDegrees);
            }
            else if(message == "l90") {
              gyro.update();
              turnLeft(gyro.getHeading());
            }
            else if(message == "r90") {
              gyro.update();
              turnRight(gyro.getHeading());
            }
            else if(message == "w") {
              waitStop();
            }
            /*else if(message[0] == 'm') {
              message.remove(0, 0);
              Serial.println(message);
              goForward(message.toDouble());
            }*/
            else { 
              goForward(message.toDouble());
            }
            
            
        });
    }
}

// Start server with terminal: /usr/local/sbin/mosquitto

// Start sketch

// In terminal write: mosquitto_pub -h 127.0.0.1 -t / -m "MESSAGE HERE"
// and it will show up in serial.

// To subscribe in terminal write: mosquitto_sub -h 127.0.0.1 -t /


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
  double startDistance = ((rightOdometer.getDistance() + leftOdometer.getDistance()) / 2);
  do {
    currentDistance = ((rightOdometer.getDistance() + leftOdometer.getDistance()) / 2);
    car.setSpeed(manualSpeed);
    car.setAngle(0);
    Serial.println(currentDistance);
    Serial.println(distance);
  } while(currentDistance < startDistance + distance);
  car.setSpeed(0);
  car.setAngle(0);
}


void turnLeft(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    const double SPEED_REDUCE = 0.6;

    int gyroCurrent = startGyro;
    
    do {
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      gyro.update();

      gyroCurrent = gyro.getHeading();
      
    } while(((gyroCurrent + 180) % 360 != (startGyro + 180 + 90) % 360 ));
    
      rightMotor.setSpeed(0);
      leftMotor.setSpeed(0);
}

void turnRight(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    const double SPEED_REDUCE = 0.6;


    int gyroCurrent = startGyro;

    do {
      rightMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
    } while((gyroCurrent + 180) % 360 != abs(startGyro + 180 - 90) % 360 );
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void faceForward(int startGyro){
  gyro.update();
  int gyroCurrent = startGyro;
  
  const double SPEED_REDUCE = 0.6;
    do {
      gyroCurrent = gyro.getHeading();
      rightMotor.setSpeed(SPEED_REDUCE * manualSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * -manualSpeed);
      gyro.update();
    } while(gyroCurrent != startGyro);
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void waitStop(){
  car.setSpeed(0);
  rightMotor.setSpeed(0);
  leftMotor.setSpeed(0);


  while((leftOdometer.getSpeed() > 0.010) || (rightOdometer.getSpeed() > 0.010)){
    delay(10); 
  }
  
}
