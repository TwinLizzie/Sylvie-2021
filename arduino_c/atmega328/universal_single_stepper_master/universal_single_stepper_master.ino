 // This 2 pin code is configured for use with a Nema 23 Bipolar 1.8deg 1.16Nm (164.3oz.in) 1.5A 5.4V 57x57x56mm 4 Wires

#include <Wire.h>
// Sketch > Include Library > Manage Libraries > Search for "AccelStepper" 

void setup(){
  Serial.begin(9600);
  Serial.setTimeout(10);

    // Start the I2C Bus as Master
  Wire.begin();
}

int serialState = 0;

void loop(){
  while (Serial.available() == 0) {}
  serialState = Serial.parseInt();

  Serial.print("Received command: ");
  Serial.println(serialState); 

    if (serialState == 2) {
      Wire.beginTransmission(0x04);
      Wire.write(48);
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(50);                                                            
      Wire.endTransmission();
    }
    else if (serialState == 3) {
      Wire.beginTransmission(0x04);
      Wire.write(48);      
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(51);    
      Wire.endTransmission();
    }
    else if (serialState == 4) {
      Wire.beginTransmission(0x04);
      Wire.write(48);    
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(52);      
      Wire.endTransmission();    
    }    
    else if (serialState == 5) {
      Wire.beginTransmission(0x04);
      Wire.write(48); 
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(53);          
      Wire.endTransmission();      
    }                               
    else if (serialState == 6) {
      Wire.beginTransmission(0x04);
      Wire.write(48); 
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(54);          
      Wire.endTransmission();    
    }  
    else if (serialState == 7) {
      Wire.beginTransmission(0x04);
      Wire.write(48); 
      Wire.write(50);   
      Wire.write(48); 
      Wire.write(48); 
      Wire.write(55);          
      Wire.endTransmission();   
    }          
}  
