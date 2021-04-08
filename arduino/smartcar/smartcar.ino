#include <Smartcar.h>

const int TRIGGER_PIN           = 6; // D6
const int ECHO_PIN              = 7; // D7
const unsigned int MAX_DISTANCE = 1000;
const int fSpeed   = 70;  // 70% of the full speed forward
const int bSpeed   = -70; // 70% of the full speed backward
const int lDegrees = -90; // degrees to turn left
const int rDegrees = 90;  // degrees to turn right

const int FRONT_IR_PIN = 0;
const int LEFT_IR_PIN = 1;
const int RIGHT_IR_PIN = 2;

ArduinoRuntime arduinoRuntime;
SR04 front(arduinoRuntime, TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
BrushedMotor leftMotor(arduinoRuntime, smartcarlib::pins::v2::leftMotorPins);
BrushedMotor rightMotor(arduinoRuntime, smartcarlib::pins::v2::rightMotorPins);
DifferentialControl control(leftMotor, rightMotor);
const int GYROSCOPE_OFFSET = 37;
GY50 gyro(arduinoRuntime, GYROSCOPE_OFFSET);

GP2Y0A21 frontIR(arduinoRuntime, FRONT_IR_PIN);
GP2Y0A21 leftIR(arduinoRuntime, LEFT_IR_PIN);
GP2Y0A21 rightIR(arduinoRuntime, RIGHT_IR_PIN);

const unsigned long LEFT_PULSES_PER_METER  = 600;
const unsigned long RIGHT_PULSES_PER_METER = 740;

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



SimpleCar car(control);

void setup()
{
    Serial.begin(9600);
}

void loop()
{

  obstacleAvoid();
    
}

// TODO
/*
 * Dont turn back to face forward when it should go right
 */

void obstacleAvoid(){
  int distance = front.getDistance();
  
  if(distance > 0 && distance < 100){
    // 0 left is free, 1 right is free
    int checkResults = checkSides();
    if(checkResults == 2){
      gyro.update();
      int startGyro = gyro.getHeading();
      int gyroCurrent = startGyro;
      
      turnLeft(startGyro);
      turnLeft(startGyro);
      
      car.setSpeed(fSpeed);
      car.setAngle(0);
      delay(100);
    }
    else if(checkResults == 0) {
      gyro.update();
      turnLeft(gyro.getHeading());
      car.setSpeed(fSpeed);
      car.setAngle(0);
      delay(100);
    } else {
      gyro.update();
      turnRight(gyro.getHeading());
      car.setSpeed(fSpeed);
      car.setAngle(0);
      delay(1000);
    }
  }
  else if(distance > 0 && distance < 200){ // slow down more
    car.setSpeed(0.3 * fSpeed);
    car.setAngle(0);
  }
  else if(distance > 0 && distance < 300){ // slow down
    car.setSpeed(0.5 * fSpeed);
    car.setAngle(0);
  }
  
  car.setSpeed(fSpeed);
  car.setAngle(0);
  delay(100);
}


// Rotates 90 degrees left, then 180 right (90 degrees right from start)
int checkSides() {
    waitStop();
    Serial.println("Checking sides");
    gyro.update();
    
    int startGyro = gyro.getHeading();
    int gyroCurrent = startGyro;
    int distances [2] = {0,0}; 

    turnLeft(startGyro);
    distances[0] = front.getDistance();
    
    turnRight(startGyro);
    distances[1] = front.getDistance();
    
    faceForward(startGyro);

    Serial.println(distances[0]);
    Serial.println(distances[1]);
    
    if((distances[0] < 100) && (distances[1] < 100) && (distances[0] > 0) && (distances[1] > 0)){
      Serial.println("Returned 2");
      return 2;
    }
    else if(distances[0] == 0){
      Serial.println("Returned 0");
      return 0;
    }
    else if((distances[0] > distances[1])){
      Serial.println("Returned 0");
      return 0;
    } else {
      Serial.println("Returned 1");
      return 1;
    }
    
}

void turnLeft(int startGyro){
    gyro.update();
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
    const double SPEED_REDUCE = 0.6;

    int gyroCurrent = startGyro;
    
    do {
      rightMotor.setSpeed(SPEED_REDUCE * fSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * bSpeed);
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
      rightMotor.setSpeed(SPEED_REDUCE * bSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * fSpeed);
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
      rightMotor.setSpeed(SPEED_REDUCE * fSpeed);
      leftMotor.setSpeed(SPEED_REDUCE * bSpeed);
      gyro.update();
    } while(gyroCurrent != startGyro);
    rightMotor.setSpeed(0);
    leftMotor.setSpeed(0);
}

void waitStop(){
  car.setSpeed(0);
  rightMotor.setSpeed(0);
  leftMotor.setSpeed(0);


  while((leftOdometer.getSpeed() > 0) || (rightOdometer.getSpeed() > 0)){
    delay(10); 
  }
  
}



void handleInput()
{ // handle serial input if there is any
    if (Serial.available())
    {
        char input = Serial.read(); // read everything that has been received so far and log down
                                    // the last entry
        switch (input)
        {
        case 'a': // rotate counter-clockwise going forward
            car.setSpeed(fSpeed);
            car.setAngle(lDegrees);
            break;
        case 'd': // turn clock-wise
            car.setSpeed(fSpeed);
            car.setAngle(rDegrees);
            break;
        case 'w': // go ahead
            car.setSpeed(fSpeed);
            car.setAngle(0);
            break;
        case 's': // go back
            car.setSpeed(bSpeed);
            car.setAngle(0);
            break;
        case 'c': // go back
            checkSides();
            break;
        default: // if you receive something that you don't know, just stop
            car.setSpeed(0);
            car.setAngle(0);
        }
        
    }
}
