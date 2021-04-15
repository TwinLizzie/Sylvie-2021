#include <Wire.h>

String serialState = "";
int stepperState = 0;
char gbxValues[] = "";
char *gbxName = NULL;

int L1_address = 0x13;
int L2_address = 0x15;
int L3_address = 0x17;

int R1_address = 0x14;
int R2_address = 0x16;
int R3_address = 0x18;

void setup(){
  Serial.begin(9600);
  Serial.setTimeout(10);

  Wire.begin();
}

String getValue(String data, char separator, int index){
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
      found++;
      strIndex[0] = strIndex[1]+1;
      strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void moveGearbox(int gbx_v, int gbx_add){
  if (gbx_v > 0){
    int val_digit1 = 48 + ((gbx_v / 1000) % 10);
    int val_digit2 = 48 + ((gbx_v / 100) % 10);
    int val_digit3 = 48 + ((gbx_v / 10) % 10);
    int val_digit4 = 48 + (gbx_v % 10);
    
    Wire.beginTransmission(gbx_add);
    Wire.write(48);
    Wire.write(val_digit1);
    Wire.write(val_digit2);
    Wire.write(val_digit3);
    Wire.write(val_digit4);
    Wire.endTransmission(); 
  }
}

void loop(){
  if (Serial.available() > 0){
    serialState = Serial.readStringUntil('\n');    
    
    int L1_gbx = getValue(serialState,',',0).toInt();
    int L2_gbx = getValue(serialState,',',1).toInt();
    int L3_gbx = getValue(serialState,',',2).toInt();
    int R1_gbx = getValue(serialState,',',3).toInt();
    int R2_gbx = getValue(serialState,',',4).toInt();
    int R3_gbx = getValue(serialState,',',5).toInt();
    
    Serial.print("Received Gearbox Values: ");
    Serial.print(L1_gbx);
    Serial.print(", ");
    Serial.print(L2_gbx);
    Serial.print(", ");
    Serial.print(L3_gbx);
    Serial.print(", ");
    Serial.print(R1_gbx);
    Serial.print(", ");
    Serial.print(R2_gbx);
    Serial.print(", ");
    Serial.println(R3_gbx);

    moveGearbox(L1_gbx, L1_address);
    moveGearbox(L2_gbx, L2_address);
    moveGearbox(L3_gbx, L3_address);
    moveGearbox(R1_gbx, R1_address);
    moveGearbox(R2_gbx, R2_address);
    moveGearbox(R3_gbx, R3_address);
  }
}
