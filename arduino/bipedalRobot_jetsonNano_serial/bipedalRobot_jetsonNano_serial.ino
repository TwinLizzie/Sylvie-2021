#include <Wire.h>

String serialState = "";
int stepperState = 0;
char gbxValues[] = "";
char *gbxName = NULL;

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

void moveGearbox(byte address, )

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
  }
}
