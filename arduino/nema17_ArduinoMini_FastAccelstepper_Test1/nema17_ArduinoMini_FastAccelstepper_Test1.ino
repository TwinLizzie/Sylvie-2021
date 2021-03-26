#include "FastAccelStepper.h"

#define dirPinStepper    2
#define enablePinStepper 4
#define stepPinStepper   9  // OC1A in case of AVR

int stepperState = 0;

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepper = NULL;

void setup() {
  engine.init();
  stepper = engine.stepperConnectToPin(stepPinStepper);
  if (stepper) {
    stepper->setDirectionPin(dirPinStepper);
    stepper->setEnablePin(enablePinStepper);
    stepper->setAutoEnable(true);

    stepper->setSpeed(15);       // the parameter is us/step !!!
    stepper->setAcceleration(45000);
  }
}

void loop() {
  stepper->moveTo(200000);
}
