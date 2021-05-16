#include <Arduino.h>
#include <Wire.h>
#include <WirePacker.h>
#include <Adafruit_PWMServoDriver.h>

#define I2C_SLAVE_ADDR 0x60
#define SERVOMIN  125 //  minimum pulse length count (out of 4096)
#define SERVOMAX  600 // maximum pulse length count (out of 4096)

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);

int serialState = 0;

uint8_t sg90_1 = 0;
uint8_t sg90_2 = 1;
uint8_t sg90_3 = 2;
uint8_t sg90_4 = 3;
uint8_t sg90_5 = 4;

uint8_t MG996R_0 = 5;
uint8_t MG996R_1 = 6;

void setup()
{
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  pwm.setPWM(sg90_1, 0, angleToPulse(90));
  pwm.setPWM(sg90_2, 0, angleToPulse(90));

  pwm.setPWM(sg90_3, 0, angleToPulse(90));
  pwm.setPWM(sg90_4, 0, angleToPulse(90));

  pwm.setPWM(sg90_5, 0, angleToPulse(90));

  pwm.setPWM(MG996R_0, 0, angleToPulse(90));
  pwm.setPWM(MG996R_1, 0, angleToPulse(90));
  
  Serial.begin(115200);
  Serial.setTimeout(10);
    
  Wire.begin();
}

int angleToPulse(int ang){
   int pulse = map(ang,0, 180, SERVOMIN,SERVOMAX);// map angle of 0 to 180 to Servo min and Servo max 
   return pulse;
}

void loop(){
  if (Serial.available()) {
    serialState = Serial.parseInt();
    
    Serial.print("Received command: ");
    Serial.println(serialState);     
  }  

  //static byte x = 1; // Number of Stepper motor!

  if (serialState > 0){ 
    WirePacker packer;

    packer.write("0");
    switch (serialState) {
      case 2:
        packer.write("20061");
        break;
      case 3:      
        packer.write("20071");
        break;
      case 4:    
        packer.write("20062");
        break;
      case 5:
        packer.write("20072");
        break;
      case 6:
        packer.write("20063");
        break;
      case 7:
        packer.write("20073");
        break;
      case 8:
        packer.write("20064");
        break;
      case 9:
        packer.write("20074");
        break;   
      case 10:
        pwm.setPWM(MG996R_0, 0, angleToPulse(180)); 
        break;
      case 11:
        pwm.setPWM(MG996R_0, 0, angleToPulse(0)); 
        break; 
      case 12:
        pwm.setPWM(MG996R_1, 0, angleToPulse(160)); 
        delay(150);      
        pwm.setPWM(MG996R_1, 0, angleToPulse(140));
        delay(150);          
        pwm.setPWM(MG996R_1, 0, angleToPulse(60)); 
        break;
      case 13:
        pwm.setPWM(MG996R_1, 0, angleToPulse(112)); 
        delay(150);  
        pwm.setPWM(MG996R_1, 0, angleToPulse(130)); 
        delay(150);    
        pwm.setPWM(MG996R_1, 0, angleToPulse(180));
        break;  
      case 14:
        pwm.setPWM(sg90_1, 0, angleToPulse(180)); 
        break;  
      case 15:
        pwm.setPWM(sg90_1, 0, angleToPulse(0));
        break;
      case 16:
        pwm.setPWM(sg90_2, 0, angleToPulse(180));
        break;
      case 17:
        pwm.setPWM(sg90_2, 0, angleToPulse(0));
        break;
      case 18:
        pwm.setPWM(sg90_3, 0, angleToPulse(180)); 
        break;
      case 19:
        pwm.setPWM(sg90_3, 0, angleToPulse(0)); 
        break;
      case 20:
        pwm.setPWM(sg90_4, 0, angleToPulse(180));
        break;
      case 21:
        pwm.setPWM(sg90_4, 0, angleToPulse(0));
        break;
      case 22:
        pwm.setPWM(sg90_5, 0, angleToPulse(180)); 
        break;
      case 23:
        pwm.setPWM(sg90_5, 0, angleToPulse(0)); 
        break;                  
      break;
    }  
    //packer.write(x);
    packer.end();    
  
    Wire.beginTransmission(I2C_SLAVE_ADDR);
    while (packer.available()) {    // write every packet byte
      Wire.write(packer.read()); 
    }
    Wire.endTransmission();    
    serialState = 0;
  }
}
