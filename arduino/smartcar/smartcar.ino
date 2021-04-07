#include <Smartcar.h>
const int TRIGGER_PIN           = 6; 
const int ECHO_PIN              = 7;
const unsigned int MAX_DISTANCE = 1000;
ArduinoRuntime arduinoRuntime;
SR04 sensor(arduinoRuntime, TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
BrushedMotor leftMotor(arduinoRuntime, smartcarlib::pins::v2::leftMotorPins);
BrushedMotor rightMotor(arduinoRuntime, smartcarlib::pins::v2::rightMotorPins);
DifferentialControl control(leftMotor, rightMotor);
SimpleCar car(control);

int const stop_dist = 200;



void setup() {
  Serial.begin(9600);
  car.setSpeed(60);
  
}

void loop() {
  if(sensor.getDistance() > 0 && sensor.getDistance() < stop_dist){
    car.setSpeed(0);
  }
 
}
