// Slave code for Sylvie 2021 Neck Z axis using Arduino Nano/Mini
// This 2 pin code is configured for use with a Nema 23 Bipolar 1.8deg 1.16Nm (164.3oz.in) 1.5A 5.4V 57x57x56mm 4 Wires

#include <AccelStepper.h>
#include <Wire.h>

//int i2cMessage = 0;
int i2cAddress = 0x20;

// Stepper motor config
int microstepRes = 8;

int stepperSpeed = 1200 * microstepRes; //maximum steps per second
int motorAccel = 300 * microstepRes; //steps/second/second to accelerate

int gearReduction = 5;
int stepsPerRev = 100; // e.g. one full revolution is 200 at 1.8deg. 100 for half. 50 for quarter.. etc.

//int resetPin = 5;
//int m2Pin = 6;
//int m1Pin = 7;
//int m0Pin = 8;  
int enablePin = 4; // Turn motor driver on/off (can save power when motor is idle)

//set up the accelStepper intance
//the "1" tells it we are using a driver (DRV8825 or other)
AccelStepper stepper_one(1, 9, 2);//Step, Dir

void setup(){
  Wire.begin(i2cAddress);
  Wire.onReceive(receiveEvent);
  
  stepper_one.setMaxSpeed(stepperSpeed);
  stepper_one.setSpeed(stepperSpeed);
  stepper_one.setAcceleration(motorAccel);

  //digitalWrite(m2Pin, LOW);
  //digitalWrite(m1Pin, LOW);
  //digitalWrite(m0Pin, HIGH);

  //digitalWrite(resetPin, HIGH);
}

int stepperState = 0;

void receiveEvent(int bytes) {
  stepperState = Wire.read();    // read one character from the I2C
}

void loop(){
  digitalWrite(enablePin, HIGH);
  if(stepperState > 0) {
    
    if(stepperState == 50){
        stepper_one.move(10 * 4.28 * microstepRes); //Move X times revolutions, according to gear reduction ratio.
        stepperState = 0;
    }
    else if(stepperState == 51){    
        stepper_one.move(-10 * 4.28 * microstepRes);  
        stepperState = 0;                      
    }
    else if(stepperState == 52){
        stepper_one.move(20 * 4.28 * microstepRes);
        stepperState = 0;         
    }
    else if(stepperState == 53){
        stepper_one.move(-20 * 4.28 * microstepRes);
        stepperState = 0;         
    }
    else if(stepperState == 54){
        stepper_one.move(30 * 4.28 * microstepRes);
        stepperState = 0;         
    }
    else if(stepperState == 55){
        stepper_one.move(-30 * 4.28 * microstepRes);
        stepperState = 0;         
    }
  }
  
  while (stepper_one.distanceToGo() != 0) {
      digitalWrite(enablePin, LOW);
      stepper_one.run();
  }
}  
