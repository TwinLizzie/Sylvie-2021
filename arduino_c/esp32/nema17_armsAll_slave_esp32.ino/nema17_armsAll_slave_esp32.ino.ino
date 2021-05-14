
// Slave code for Sylvie 2021 Robot Legs using Arduino Nano/Mini
// This 2 pin code is configured for use with a Nema 23 Bipolar 1.8deg 1.16Nm (164.3oz.in) 1.5A 5.4V 57x57x56mm 4 Wires

#include <FastAccelStepper.h>
#include <WireSlave.h>

#define dirPinStepper_ElbowX    25
#define enablePinStepper_ElbowX 27
#define stepPinStepper_ElbowX  26  // OC1A in case of AVR

#define dirPinStepper_ElbowZ 2
#define enablePinStepper_ElbowZ 33
#define stepPinStepper_ElbowZ 32

#define dirPinStepper_ShoulderY 17
#define enablePinStepper_ShoulderY 14
#define stepPinStepper_ShoulderY 16

#define dirPinStepper_ShoulderX 23
#define enablePinStepper_ShoulderX 18
#define stepPinStepper_ShoulderX 19 

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepperElbowX = NULL;
FastAccelStepper *stepperElbowZ = NULL;
FastAccelStepper *stepperShoulderY = NULL;
FastAccelStepper *stepperShoulderX = NULL;

#define SDA_PIN 21
#define SCL_PIN 22
#define I2C_SLAVE_ADDR 0x60

int bevelGear = (24 / 12);
int gearRatio = 53.575757576;
int stepsPerRev = 20;
int microsteps = 4;

long formula = ((((stepsPerRev * gearRatio) * microsteps) / 360) * bevelGear);
long formula2 = (((stepsPerRev * gearRatio) * microsteps) / 360);

int currentAngle[5] = {0, 1000, 1000, 1000, 1000};
int newAngle[5] = {0, 0, 0, 0, 0};

// receiveEvent Variables

String currentStatus = "";
String chosenStepper = "";

int stepperState = 0;
int wireState = 0;

char readChar[40];
boolean flagRx = false;

void setup() {
  Serial.begin(115200);

  bool success = WireSlave.begin(SDA_PIN, SCL_PIN, I2C_SLAVE_ADDR);
  if (!success) {
    Serial.println("I2C slave init failed");
    while(1) delay(100);
  }
  else {
    Serial.println("I2C slave init success!"); 
  }
  
  WireSlave.onReceive(receiveEvent);

  engine.init();
  
  stepperElbowX = engine.stepperConnectToPin(stepPinStepper_ElbowX);
  if (stepperElbowX) {
    stepperElbowX->setDirectionPin(dirPinStepper_ElbowX);
    stepperElbowX->setEnablePin(enablePinStepper_ElbowX);
    stepperElbowX->setAutoEnable(true);

    stepperElbowX->setSpeedInUs(250);       // the parameter is us/step !!!
    stepperElbowX->setAcceleration(15000);
  }

  stepperElbowZ = engine.stepperConnectToPin(stepPinStepper_ElbowZ);
  if (stepperElbowZ) {
    stepperElbowZ->setDirectionPin(dirPinStepper_ElbowZ);
    stepperElbowZ->setEnablePin(enablePinStepper_ElbowZ);
    stepperElbowZ->setAutoEnable(true);

    stepperElbowZ->setSpeedInUs(250);       // the parameter is us/step !!!
    stepperElbowZ->setAcceleration(15000);
  }  


  stepperShoulderY = engine.stepperConnectToPin(stepPinStepper_ShoulderY);
  if (stepperShoulderY) {
    stepperShoulderY->setDirectionPin(dirPinStepper_ShoulderY);
    stepperShoulderY->setEnablePin(enablePinStepper_ShoulderY);
    stepperShoulderY->setAutoEnable(true);

    stepperShoulderY->setSpeedInUs(250);       // the parameter is us/step !!!
    stepperShoulderY->setAcceleration(15000);
  }    

  stepperShoulderX = engine.stepperConnectToPin(stepPinStepper_ShoulderX);
  if (stepperShoulderX) {
    stepperShoulderX->setDirectionPin(dirPinStepper_ShoulderX);
    stepperShoulderX->setEnablePin(enablePinStepper_ShoulderX);
    stepperShoulderX->setAutoEnable(true);

    stepperShoulderX->setSpeedInUs(250);       // the parameter is us/step !!!
    stepperShoulderX->setAcceleration(15000);
  }   
}

void receiveEvent(int byteCount) {
  currentStatus = "";
  chosenStepper = "";

  int i;
  for (i = 0; i < byteCount; i++)
  {
    readChar[i] = WireSlave.read();     // receive byte as a character
    Serial.println(readChar[i]);
  }
  readChar[i] = '\0';  // assume it is a string, add zero-terminator
  flagRx = true;    // set flag, we received something.
}

void moveChosenStepper(int numSteps, int stepperChoice){
  if (stepperChoice == 1){
    stepperElbowX->setSpeedInUs(250);       // the parameter is us/step !!!
    stepperElbowX->setAcceleration(15000);
    stepperElbowX->move(numSteps * formula);  
  }
  else  if (stepperChoice == 2){
    stepperElbowZ->setSpeedInUs(250);       // the parameter is us/step !!!
    stepperElbowZ->setAcceleration(15000);
    stepperElbowZ->move(numSteps * formula2);  
  }
  else  if (stepperChoice == 3){
    stepperShoulderY->setSpeedInUs(250);       // the parameter is us/step !!!
    stepperShoulderY->setAcceleration(15000);
    stepperShoulderY->move(numSteps * formula);  
  }  
  else  if (stepperChoice == 4){
    stepperShoulderX->setSpeedInUs(250);       // the parameter is us/step !!!
    stepperShoulderX->setAcceleration(15000);
    stepperShoulderX->move(numSteps * formula2);  
  }   
}

void loop() {
  WireSlave.update();

  delay(1);
  
  if (flagRx) {
    currentStatus += readChar[1];
    currentStatus += readChar[2];
    currentStatus += readChar[3];
    currentStatus += readChar[4];

    chosenStepper += readChar[5];

    stepperState = chosenStepper.toInt();
    wireState = currentStatus.toInt();

    Serial.print("Wire state: ");
    Serial.print(wireState);
    Serial.print(", Stepper: ");
    Serial.println(stepperState);
    
    flagRx = false;
  }

  if (wireState > 0) {  
    if (wireState > 0 && wireState < 2000) {
      newAngle[stepperState] = (wireState - currentAngle[stepperState]);  
      moveChosenStepper(newAngle[stepperState], stepperState);
      currentAngle[stepperState] = wireState;
    }
    
    else{
      switch(wireState){
        case 2002:
          moveChosenStepper(1, stepperState);
          break;
        case 2003:
          moveChosenStepper(-1, stepperState);
          break;
        case 2004:
          moveChosenStepper(20, stepperState);
          break;
        case 2005:
          moveChosenStepper(-20, stepperState);
          break;
        case 2006:
          moveChosenStepper(30, stepperState);
          break;
        case 2007:
          moveChosenStepper(-30, stepperState);
          break;
        break;  
      }
    }
    
    wireState = 0;
  }
}
