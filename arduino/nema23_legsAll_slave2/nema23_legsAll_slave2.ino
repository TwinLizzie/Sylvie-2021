// Slave code for Sylvie 2021 Neck X axis using Arduino Nano/Mini
// This 2 pin code is configured for use with a Nema 23 Bipolar 1.8deg 1.16Nm (164.3oz.in) 1.5A 5.4V 57x57x56mm 4 Wires

#include <AccelStepper.h>
#include <Wire.h>

int i2cAddress = 0x16;

// Stepper motor config
int microstepRes = 4;
int stepperSpeed = 1200 * microstepRes; //maximum steps per second
int motorAccel = 1000 * microstepRes; //steps/second/second to accelerate
 
int enablePin = 4; // Turn motor driver on/off (can save power when motor is idle)

// Movement Variables

int currentAngle = 1000;
int newAngle = 0;

// receiveEvent Variables

String currentStatus = "";
int wireState = 0;
char readChar[40];
boolean flagRx = false;

//set up the accelStepper intance
//the "1" tells it we are using a driver (DRV8825 or other)
AccelStepper stepper_one(1, 3, 2);//Step, Dir

void setup(){
  Wire.begin(i2cAddress);
  Wire.onReceive(receiveEvent);
  
  stepper_one.setMaxSpeed(stepperSpeed);
  stepper_one.setSpeed(stepperSpeed);
  stepper_one.setAcceleration(motorAccel);

  Serial.begin(9600);
  Serial.setTimeout(10);

  Serial.println("Waiting for angles!");
}

void receiveEvent(int byteCount) {
  currentStatus = "";
   
  int i;
  for (i=0; i<byteCount; i++)
  {
    readChar[i] = Wire.read();     // receive byte as a character
  }
  readChar[i] = '\0';  // assume it is a string, add zero-terminator
  flagRx = true;    // set flag, we received something.
}

void loop(){
  digitalWrite(enablePin, HIGH);
  if (flagRx) {
    currentStatus += readChar[1];
    currentStatus += readChar[2];
    currentStatus += readChar[3];
    currentStatus += readChar[4];

    wireState = currentStatus.toInt();    
    
    Serial.println(wireState);
    flagRx = false;
  } 

  if (wireState > 0) {
    if(wireState == 2000){
      stepper_one.move(1 * ((((200 * 53.575757576) * 4) / 360) * 2));     
      currentAngle++;
      wireState = 0;  
    }
    else if(wireState == 2001){
      stepper_one.move(-1 * ((((200 * 53.575757576) * 4) / 360) * 2)); 
      currentAngle--;
      wireState = 0;       
    }
    else if(wireState == 2002){
      stepper_one.move(1 * ((((200 * 53.575757576) * 4) / 360) * 2));     
      wireState = 0;  
    }
    else if(wireState == 2003){
      stepper_one.move(-1 * ((((200 * 53.575757576) * 4) / 360) * 2)); 
      wireState = 0;       
    }    
    else if(wireState > 0 && wireState < 2000){
      newAngle = (wireState - currentAngle);
      stepper_one.move(newAngle * ((((20 * 53.575757576) * 4) / 360) * 2)); //Move X times revolutions, according to gear reduction ratio. 
      currentAngle = wireState; 

      wireState = 0;
    }
  }
    
  
  while (stepper_one.distanceToGo() != 0) {
    digitalWrite(enablePin, LOW);   
    stepper_one.run();
  }
}  
