#include <AccelStepper.h>
#include <Wire.h>

// Stepper motor config
int microstepRes = 4;

int stepperSpeed = 1200 * microstepRes; //maximum steps per second
int motorAccel = 800 * microstepRes; //steps/second/second to accelerate

int enablePin = 4; // Turn motor driver on/off (can save power when motor is idle)

AccelStepper stepper_one(1, 3, 2);

void setup() {
  stepper_one.setMaxSpeed(stepperSpeed);
  stepper_one.setSpeed(stepperSpeed);
  stepper_one.setAcceleration(motorAccel);

  Serial.begin(9600);
  Serial.setTimeout(10); 

  // Start the I2C Bus as Master
  Wire.begin();   
}

int serialState = 0;
int stepperState = 0;

void loop() {
  digitalWrite(enablePin, HIGH);
  
  while (Serial.available() == 0) {}
  serialState = Serial.parseInt(); 
  
  Serial.print("Received command: ");
  Serial.println(serialState);    

  if(serialState > 0) { 
    
    if(serialState > 1000 && serialState < 2000){
      if(serialState == 1500){
        stepper_one.move(1 * ((((200 * 53.575757576) * 4) / 360) * 2));        
      }
      else if(serialState == 1501){
        stepper_one.move(-1 * ((((200 * 53.575757576) * 4) / 360) * 2));   
      }
      else if(serialState < 1200){
        stepperState = serialState - 1000;
        stepper_one.moveTo(stepperState * ((((200 * 53.575757576) * 4) / 360) * 2));
      }
    }
    
    else if (serialState > 2000 && serialState < 3000) {

      if(serialState == 2500){
        Wire.beginTransmission(0x40);
        Wire.write(200);
        Wire.endTransmission();        
      }
      else if(serialState == 2501){
        Wire.beginTransmission(0x40);
        Wire.write(201);
        Wire.endTransmission();       
      }
      if(serialState == 2502){
        Wire.beginTransmission(0x40);
        Wire.write(202);
        Wire.endTransmission();        
      }
      else if(serialState == 2503){
        Wire.beginTransmission(0x40);
        Wire.write(203);
        Wire.endTransmission();       
      }      
      else if(serialState < 2200){
        stepperState = serialState - 2000;
        Wire.beginTransmission(0x40);
        Wire.write(stepperState);
        Wire.endTransmission();
      }
    }
  }
  
  while (stepper_one.distanceToGo() != 0) {
    digitalWrite(enablePin, LOW);   
    stepper_one.run();
  }
}
