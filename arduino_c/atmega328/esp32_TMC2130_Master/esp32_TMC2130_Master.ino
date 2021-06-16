#include <Arduino.h>
#include <Wire.h>
#include <WirePacker.h>

#define I2C_SLAVE_ADDR 0x60

const unsigned int MAX_MESSAGE_LENGTH = 12;

int currentSpeed = 10;
int currentAmps = 1000;
int currentAngle = 0;

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(10);
    
  Wire.begin();
}

void loop(){
 //Check to see if anything is available in the serial receive buffer
 while (Serial.available() > 0)
 {
   //Create a place to hold the incoming message
   static char message[MAX_MESSAGE_LENGTH];
   static unsigned int message_pos = 0;

   //Read the next available byte in the serial receive buffer
   char inByte = Serial.read();

   //Message coming in (check not terminating character) and guard for over message size
   if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
   {
     //Add the incoming byte to our message
     message[message_pos] = inByte;
     message_pos++;
   }
   //Full message received...
   else
   {
     //Add null character to string
     message[message_pos] = '\0';

     WirePacker packer;
     //packer.write('0');
     packer.write(message);
     packer.end();    
    
     Wire.beginTransmission(I2C_SLAVE_ADDR);
     while (packer.available()) {    // write every packet byte
       Wire.write(packer.read()); 
       //Serial.println(packer.read());
     }
     Wire.endTransmission(); 

     //Print the message (or do other things)
     if(message[0] == 'm'){
       message[0] = '0';

       if(message[1] == '-'){
         message[1] = '0';
         int newAngle = atoi(message);
         currentAngle = -newAngle;
       }else{
         currentAngle = atoi(message);
       }
       Serial.print("New angle: ");
       Serial.println(currentAngle);
     }
     else if(message[0] == 's'){
       message[0] = '0';
       int newSpeed = atoi(message);
       currentSpeed = newSpeed;
       Serial.print("New speed: ");
       Serial.println(currentSpeed);       
     }
     else if(message[0] == 'c'){
       message[0] = '0';
       if(atoi(message) <= 1200){
         int newAmps = atoi(message);
         currentAmps = newAmps;
         Serial.print("New current: ");
         Serial.println(currentAmps);
       }else{
         Serial.println("Current too high!");
       }
     }

     //Reset for the next message
     message_pos = 0;
   }
 }
}
