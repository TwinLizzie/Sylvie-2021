#include "FastAccelStepper.h"
#include "Wire.h"

#define dirPinStepper    2
#define enablePinStepper 4
#define stepPinStepper   9  // OC1A in case of AVR

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepper = NULL;

int i2cAddress = 0x20;

int gearRatio = (48 / 9);
int stepsPerRev = 200;
int microsteps = 8;
int stepperState = 0;

int formula = (microsteps * (gearRatio * stepsPerRev));

void setup() {
  Wire.begin(i2cAddress);
  Wire.onReceive(receiveEvent);
  
  engine.init();
  stepper = engine.stepperConnectToPin(stepPinStepper);
  if (stepper) {
    stepper->setDirectionPin(dirPinStepper);
    stepper->setEnablePin(enablePinStepper);
    stepper->setAutoEnable(true);

    stepper->setSpeed(60);       // the parameter is us/step !!!
    stepper->setAcceleration(10000);
  }
}

void receiveEvent(int bytes) {
  stepperState = Wire.read();    // read one character from the I2C
}

void loop() {
  switch (stepperState) {
    case 50:
      stepper->move(0.05 * formula);
      stepperState = 0;
      break;
    case 51:
      stepper->move(-0.05 * formula);  
      stepperState = 0;
      break;
    case 52:
      stepper->move(0.10 * formula);
      stepperState = 0;
      break;
    case 53:
      stepper->move(-0.10 * formula); 
      stepperState = 0;
      break;
    case 54:
      stepper->move(0.2 * formula);
      stepperState = 0;    
      break;                
    case 55:
      stepper->move(-0.2 * formula);
      stepperState = 0; 
      break;
    break;
  }
}
