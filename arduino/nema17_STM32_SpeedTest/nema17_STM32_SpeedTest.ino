 // This 2 pin code is configured for use with a Nema 23 Bipolar 1.8deg 1.16Nm (164.3oz.in) 1.5A 5.4V 57x57x56mm 4 Wires

#include <AccelStepper.h> // This can be installed by going to 
// #include <Wire.h>
// Sketch > Include Library > Manage Libraries > Search for "AccelStepper" 

int microstepRes = 8;

int stepperSpeed = 2400 * microstepRes; //maximum steps per second
int motorAccel = 4800 * microstepRes; //steps/second/second to accelerate

int stepperState = 0;

int enablePin = 4; // Turn motor driver on/off (can save power when motor is idle)

//set up the accelStepper intance
//the "1" tells it we are using a driver (DRV8825 or other)
AccelStepper stepper_one(1, 3, 2);//Step, Dir

void setup(){
  Serial.begin(9600);
  Serial.setTimeout(10);
  
  stepper_one.setMaxSpeed(stepperSpeed);
  stepper_one.setSpeed(stepperSpeed);
  stepper_one.setAcceleration(motorAccel);
  stepper_one.moveTo(5000);
}

void loop(){ 
  
  if (stepper_one.distanceToGo() == 0){
    digitalWrite(enablePin, HIGH);
  }
  else {
      digitalWrite(enablePin, LOW);
      stepper_one.run();
  }
  //while (stepper_one.distanceToGo() != 0){
  //    stepper_one.run();    
  //}
}  
