#include <Smartcar.h>

const int TRIGGER_PIN           = 6; // D6
const int ECHO_PIN              = 7; // D7
const unsigned int MAX_DISTANCE = 1000;
const int fSpeed   = 70;  // 70% of the full speed forward
const int bSpeed   = -70; // 70% of the full speed backward
const int lDegrees = -90; // degrees to turn left
const int rDegrees = 90;  // degrees to turn right

//const int SIDE_FRONT_PIN = 0; //left 1, right 2
const int LEFT_IR_PIN = 1;
const int RIGHT_IR_PIN = 2;

ArduinoRuntime arduinoRuntime;
SR04 front(arduinoRuntime, TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
BrushedMotor leftMotor(arduinoRuntime, smartcarlib::pins::v2::leftMotorPins);
BrushedMotor rightMotor(arduinoRuntime, smartcarlib::pins::v2::rightMotorPins);
DifferentialControl control(leftMotor, rightMotor);
const int GYROSCOPE_OFFSET = 37;
GY50 gyro(arduinoRuntime, GYROSCOPE_OFFSET);

GP2Y0A21 leftIR(arduinoRuntime, LEFT_IR_PIN);
GP2Y0A21 rightIR(arduinoRuntime, RIGHT_IR_PIN);

SimpleCar car(control);

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    //Serial.println(sideFrontIR.getDistance());
    //Serial.println(front.getDistance());
    delay(100);
    handleInput();
    obstacleAvoid();

    //gyro.update();
    //Serial.println(gyro.getHeading());
    
}


void obstacleAvoid(){

    int distance = front.getDistance();

    if(distance > 0 && distance < 200){ // Begin turning
      //car.setSpeed(0);
      //car.setAngle(0);
      
      //car.setSpeed(fSpeed);

      if (rightIR.getDistance() > 0){
        car.setSpeed(0.25 * fSpeed);
        car.setAngle(lDegrees);
      }
      else if (leftIR.getDistance() > 0){
        car.setSpeed(0.25 * fSpeed);
        car.setAngle(rDegrees);
      }
      else {
        car.setSpeed(0.25 * fSpeed);
        car.setAngle(lDegrees);
      }

      delay(300);
    }
    else if(distance > 0 && distance < 300){ // slow down
        car.setSpeed(0.25 * fSpeed);
        car.setAngle(0);
    }
    else if(distance > 0 && distance < 400){ // slow down more
        car.setSpeed(0.5 * fSpeed);
        car.setAngle(0);
    }
    else if(distance == 0){
      car.setSpeed(fSpeed);
      car.setAngle(0);
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
        case 'l': // rotate counter-clockwise going forward
            car.setSpeed(fSpeed);
            car.setAngle(lDegrees);
            break;
        case 'r': // turn clock-wise
            car.setSpeed(fSpeed);
            car.setAngle(rDegrees);
            break;
        case 'f': // go ahead
            car.setSpeed(fSpeed);
            car.setAngle(0);
            break;
        case 'b': // go back
            car.setSpeed(bSpeed);
            car.setAngle(0);
            break;
        default: // if you receive something that you don't know, just stop
            car.setSpeed(0);
            car.setAngle(0);
        }
        
    }
}
