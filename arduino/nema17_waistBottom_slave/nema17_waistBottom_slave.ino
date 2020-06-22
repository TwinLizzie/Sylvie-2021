// Slave code for Sylvie 2021 Neck X axis using Arduino Nano/Mini
// This 2 pin code is configured for use with a Nema 23 Bipolar 1.8deg 1.16Nm (164.3oz.in) 1.5A 5.4V 57x57x56mm 4 Wires

#include <AccelStepper.h>
#include <Wire.h>

//int i2cMessage = 0;
int i2cAddress = 0x40;

// Stepper motor config
int microstepRes = 4;

int stepperSpeed = 1200 * microstepRes; //maximum steps per second
int motorAccel = 800 * microstepRes; //steps/second/second to accelerate
 
int enablePin = 4; // Turn motor driver on/off (can save power when motor is idle)

//set up the accelStepper intance
//the "1" tells it we are using a driver (DRV8825 or other)
AccelStepper stepper_one(1, 3, 2);//Step, Dir

void setup(){
  Wire.begin(i2cAddress);
  Wire.onReceive(receiveEvent);
  
  stepper_one.setMaxSpeed(stepperSpeed);
  stepper_one.setSpeed(stepperSpeed);
  stepper_one.setAcceleration(motorAccel);
}

int wireState = 0;

void receiveEvent(int bytes) {
  wireState = Wire.read();    // read one character from the I2C
}

void loop(){
  digitalWrite(enablePin, HIGH);

  if(wireState > 0) {
    if(wireState == 200){
      stepper_one.move(1 * ((((200 * 53.575757576) * 4) / 360) * 2));     
      wireState = 0;  
    }
    else if(wireState == 201){
      stepper_one.move(-1 * ((((200 * 53.575757576) * 4) / 360) * 2)); 
      wireState = 0;       
    }
    else if(wireState < 200){
      stepper_one.moveTo(wireState * ((((200 * 53.575757576) * 4) / 360) * 2)); //Move X times revolutions, according to gear reduction ratio. 
      wireState = 0; 
    }
  }
  
  while (stepper_one.distanceToGo() != 0) {
    digitalWrite(enablePin, LOW);   
    stepper_one.run();
  }
}  
