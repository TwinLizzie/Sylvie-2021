#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  125 //  minimum pulse length count (out of 4096)
#define SERVOMAX  600 // maximum pulse length count (out of 4096)

uint8_t sg90_1 = 0;
uint8_t sg90_2 = 1;
uint8_t sg90_3 = 2;
uint8_t sg90_4 = 3;
uint8_t sg90_5 = 4;

uint8_t MG996R_0 = 5;
uint8_t MG996R_1 = 6;

void setup() {
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  pwm.setPWM(sg90_1, 0, angleToPulse(90));
  pwm.setPWM(sg90_2, 0, angleToPulse(90));

  pwm.setPWM(sg90_3, 0, angleToPulse(90));
  pwm.setPWM(sg90_4, 0, angleToPulse(90));

  pwm.setPWM(sg90_5, 0, angleToPulse(90));

  pwm.setPWM(MG996R_0, 0, angleToPulse(90));
  pwm.setPWM(MG996R_1, 0, angleToPulse(90));

  Serial.begin(9600);
  Serial.setTimeout(10); 

  // Start the I2C Bus as Master
  Wire.begin();   
}

int angleToPulse(int ang){
   int pulse = map(ang,0, 180, SERVOMIN,SERVOMAX);// map angle of 0 to 180 to Servo min and Servo max 
   return pulse;
}

long servoState = 0;

void loop() {
  while (Serial.available() == 0) {}
  servoState = Serial.parseInt();
  
  Serial.print("Received command: ");
  Serial.println(servoState);    

  if(servoState > 0) { 
  
    if(servoState == 2){
      pwm.setPWM(sg90_1, 0, angleToPulse(180));
    }
    else if(servoState == 3){
     pwm.setPWM(sg90_1, 0, angleToPulse(0));           
    }  
    else if(servoState == 4){      
     pwm.setPWM(sg90_2, 0, angleToPulse(180));  
    } 
    else if (servoState == 5){
     pwm.setPWM(sg90_2, 0, angleToPulse(0));
    }    
    else if (servoState == 6){ 
     pwm.setPWM(sg90_3, 0, angleToPulse(180));             
    }
    else if (servoState == 7){      
     pwm.setPWM(sg90_3, 0, angleToPulse(0));               
    }
    else if (servoState == 8){
     pwm.setPWM(sg90_4, 0, angleToPulse(180));
    }
    else if (servoState == 9){
     pwm.setPWM(sg90_4, 0, angleToPulse(0));  
    }
    else if (servoState == 11){   
     pwm.setPWM(sg90_5, 0, angleToPulse(160));    
    }
    else if (servoState == 12){
     pwm.setPWM(sg90_5, 0, angleToPulse(0));  
    }
    else if (servoState == 13){
     pwm.setPWM(MG996R_0, 0, angleToPulse(180));  
    }    
    else if (servoState == 14){
     pwm.setPWM(MG996R_0, 0, angleToPulse(0));  
    }    
    else if (servoState == 15){
     pwm.setPWM(MG996R_1, 0, angleToPulse(90));  
    }    
    else if (servoState == 16){
     pwm.setPWM(MG996R_1, 0, angleToPulse(70));  
    }
    else if (servoState == 17) {
      Wire.beginTransmission(0x10);
      Wire.write(50);
      Wire.endTransmission();
    }
    else if (servoState == 18) {
      Wire.beginTransmission(0x10);
      Wire.write(51);
      Wire.endTransmission();  
    }
    else if (servoState == 19){
      Wire.beginTransmission(0x20);
      Wire.write(50);
      Wire.endTransmission();  
    }  
    else if (servoState == 20){
      Wire.beginTransmission(0x20);
      Wire.write(51);
      Wire.endTransmission();  
    } 
    Serial.begin(9600);
    Serial.setTimeout(10);  
  }
}
