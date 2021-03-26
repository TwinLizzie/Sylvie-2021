 // This 2 pin code is configured for use with a Nema 23 Bipolar 1.8deg 1.16Nm (164.3oz.in) 1.5A 5.4V 57x57x56mm 4 Wires

#include <AccelStepper.h> // This can be installed by going to 
#include <Wire.h>
// Sketch > Include Library > Manage Libraries > Search for "AccelStepper" 

int microstepRes = 4;

int stepperSpeed = 1200 * microstepRes; //maximum steps per second
int motorAccel = 2400 * microstepRes; //steps/second/second to accelerate

// int gearReduction = 53.575757576;
// int stepsPerRev = 200; // e.g. one full revolution is 200 at 1.8deg. 100 for half. 50 for quarter.. etc.

int resetPin = 5;
int m2Pin = 6;
int m1Pin = 7;
int m0Pin = 8; 
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

  //digitalWrite(m2Pin, LOW);
  //digitalWrite(m1Pin, LOW);
  //digitalWrite(m0Pin, HIGH); 

  //digitalWrite(resetPin, HIGH);

    // Start the I2C Bus as Master
  Wire.begin();
}

int serialState = 0;
int stepperState = 0;

void loop(){
  digitalWrite(enablePin, HIGH);
  
  while (Serial.available() == 0) {}
  serialState = Serial.parseInt();

  Serial.print("Received command: ");
  Serial.println(stepperState); 

    if (serialState == 2) {
      Wire.beginTransmission(0x10);
      Wire.write(48);
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(50);                                                            
      Wire.endTransmission();
    }
    else if (serialState == 3) {
      Wire.beginTransmission(0x10);
      Wire.write(48);      
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(51);    
      Wire.endTransmission();
    }
    else if (serialState == 4) {
      Wire.beginTransmission(0x13);
      Wire.write(48);    
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(52);      
      Wire.endTransmission();

      Wire.beginTransmission(0x14);
      Wire.write(48);    
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(52);      
      Wire.endTransmission();      
    }    
    else if (serialState == 5) {
      Wire.beginTransmission(0x13);
      Wire.write(48); 
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(53);          
      Wire.endTransmission();

      Wire.beginTransmission(0x14);
      Wire.write(48); 
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(53);          
      Wire.endTransmission();      
    }                               
    else if (serialState == 6) {
      Wire.beginTransmission(0x13);
      Wire.write(48); 
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(54);          
      Wire.endTransmission();

      Wire.beginTransmission(0x14);
      Wire.write(48); 
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(54);          
      Wire.endTransmission();      
    }  
    else if (serialState == 7) {
      Wire.beginTransmission(0x13);
      Wire.write(48); 
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(55);          
      Wire.endTransmission();

      Wire.beginTransmission(0x14);
      Wire.write(48); 
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(55);          
      Wire.endTransmission();      
    }          
}  
