#include <Smartcar.h>

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
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  handleInput();
}


// Handle input inspired by Lecturer Dimitris Platis
// original: https://github.com/platisd/smartcar_shield/blob/master/examples/Car/manualControl/manualControl.ino
// Modifications made: changed input keys and added Q to slow down car and E to increase speed (by 10)
void handleInput()
{ // handle serial input if there is any
    if (Serial.available())
    {

        char input = Serial.read(); // read everything that has been received so far and log down
                                    // the last entry
        switch (input)
        {
        case 'a': // rotate counter-clockwise going forward
            car.setSpeed(manualSpeed);
            car.setAngle(lDegrees);
            break;
        case 'd': // turn clock-wise
            car.setSpeed(manualSpeed);
            car.setAngle(rDegrees);
            break;
        case 'w': // go ahead
            car.setSpeed(manualSpeed);
            car.setAngle(0);
            goingForward = true;
            break;
        case 's': // go back
            car.setSpeed(-manualSpeed);
            car.setAngle(0);
            goingForward = false;
            break;
        case 'q':  // Decrease speed by 10
            if ((manualSpeed - 10) >= 0) { // to stop the car from reversing when decrasing speed
                manualSpeed = manualSpeed - 10;
                Serial.println(manualSpeed);
                if (goingForward) {
                  car.setSpeed(manualSpeed);
                } else {
                  car.setSpeed(-manualSpeed);
                }
            }
            break;
        case 'e': // Increase speed by 10
            if ((manualSpeed + 10) <= 100) { // car can't go faster than 100
                manualSpeed = manualSpeed + 10;
                Serial.println(manualSpeed);
                if (goingForward) {
                  car.setSpeed(manualSpeed);
                } else {
                  car.setSpeed(-manualSpeed);
                }
            }
            break;
        default: // if you receive something that you don't know, just stop
            car.setSpeed(0);
            car.setAngle(0);
        }
        
    }
}
