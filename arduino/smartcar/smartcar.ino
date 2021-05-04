#include <Smartcar.h>
const int fSpeed   = 70;  // 70% of the full speed forward
const int bSpeed   = -70; // 70% of the full speed backward
ArduinoRuntime arduinoRuntime;
BrushedMotor leftMotor(arduinoRuntime, smartcarlib::pins::v2::leftMotorPins);
BrushedMotor rightMotor(arduinoRuntime, smartcarlib::pins::v2::rightMotorPins);
DifferentialControl control(leftMotor, rightMotor);
const int GYROSCOPE_OFFSET = 0;
const unsigned long PULSES_PER_METER = 1000;
GY50 gyro(arduinoRuntime, GYROSCOPE_OFFSET);

DirectionlessOdometer leftOdometer{
  arduinoRuntime,
  smartcarlib::pins::v2::leftOdometerPin,
  []() { leftOdometer.update(); },
  PULSES_PER_METER};
DirectionlessOdometer rightOdometer{
  arduinoRuntime,
  smartcarlib::pins::v2::rightOdometerPin,
  []() { rightOdometer.update(); },
  PULSES_PER_METER};
    
SmartCar car(arduinoRuntime, control, gyro, leftOdometer, rightOdometer);


void setup() {
  Serial.begin(9600);

}

void loop() {
  //turnTest();
  driveTest();
  

}

void turnTest(){
  int turnDegrees = 90;  //For testing purposes turnDegrees is now just set to 90. But you should be able to give the turnLeft and turnRight methods whatever value you want. 
  turnRight(turnDegrees);
  delay(5000);
  turnLeft(turnDegrees);
  delay(5000);
  
}

// Methods for turning that Adam needed. startGyro is no longer taken as an argument since it would always be zero.
// Not sure about the math for deciding how much the car should turn. Might need improvement
void turnLeft(int turnDegrees){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    const double SPEED_REDUCE = 0.3;
    int startGyro = gyro.getHeading();
    int gyroCurrent = startGyro;
    
    do {
      rightMotor.setSpeed(SPEED_REDUCE * fSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * bSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
      
    }  while((gyroCurrent + 180) % 360 != abs(startGyro + 180 + turnDegrees) % 360 );
      rightMotor.setSpeed(0);
      leftMotor.setSpeed(0);
}

void turnRight(int turnDegrees){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    const double SPEED_REDUCE = 0.3;
    int startGyro = gyro.getHeading();
    int gyroCurrent = startGyro;

    do {
      rightMotor.setSpeed(SPEED_REDUCE * bSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * fSpeed);
      gyro.update();
      gyroCurrent = gyro.getHeading();
    
    
    }  while((gyroCurrent + 180) % 360 != abs(startGyro + 180 - turnDegrees) % 360 );
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void driveTest(){
  long driveDist = 500; // For testing. This would be determined by input.
  drive(driveDist);
  delay(5000);
}

 //Drive is a method for taking a distance as a parameter and driving that distance. So far innacurate, due to rate of updating. The slower the car moves the more accurate it will be. Unsure of how to solve this drawback. 
void drive(long driveDist){          
  long startDist = car.getDistance();
  long currentDist = startDist;
  long goalDist = (startDist + driveDist);

  do{
    car.setSpeed(fSpeed);
    currentDist = car.getDistance();
  }while(currentDist < goalDist);
  car.setSpeed(0); 

}
