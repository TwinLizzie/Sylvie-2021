
// Slave code for Sylvie 2021 Robot Legs using Arduino Nano/Mini
// This 2 pin code is configured for use with a Nema 23 Bipolar 1.8deg 1.16Nm (164.3oz.in) 1.5A 5.4V 57x57x56mm 4 Wires

#include <FastAccelStepper.h>
#include <Wire.h>

#define dirPinStepper    2
#define enablePinStepper 4
#define stepPinStepper   9  // OC1A in case of AVR

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepper = NULL;

int i2cAddress = 0x12;

int bevelGear = (49 / 12);
int gearRatio = 53.575757576;
int stepsPerRev = 20;
int microsteps = 4;
int stepperState = 0;

long formula = ((((stepsPerRev * gearRatio) * microsteps) / 360) * bevelGear);

int currentAngle = 1000;
int newAngle = 0;

// receiveEvent Variables

String currentStatus = "";
int wireState = 0;
char readChar[40];
boolean flagRx = false;

void setup() {
  Wire.begin(i2cAddress);
  Wire.onReceive(receiveEvent);

  engine.init();
  stepper = engine.stepperConnectToPin(stepPinStepper);
  if (stepper) {
    stepper->setDirectionPin(dirPinStepper);
    stepper->setEnablePin(enablePinStepper);
    stepper->setAutoEnable(true);

    stepper->setSpeedInUs(250);       // the parameter is us/step !!!
    stepper->setAcceleration(15000);
  }
}

void receiveEvent(int byteCount) {
  currentStatus = "";

  int i;
  for (i = 0; i < byteCount; i++)
  {
    readChar[i] = Wire.read();     // receive byte as a character
  }
  readChar[i] = '\0';  // assume it is a string, add zero-terminator
  flagRx = true;    // set flag, we received something.
}

void loop() {
  if (flagRx) {
    currentStatus += readChar[1];
    currentStatus += readChar[2];
    currentStatus += readChar[3];
    currentStatus += readChar[4];

    wireState = currentStatus.toInt();

    Serial.println(wireState);
    flagRx = false;
  }

  if (wireState > 0) {
    if (wireState == 2000) {
      stepper->setSpeedInUs(250);       // the parameter is us/step !!!
      stepper->setAcceleration(15000);
      stepper->move(1 * formula);
      currentAngle++;
      wireState = 0;
    }
    else if (wireState == 2001) {
      stepper->setSpeedInUs(250);       // the parameter is us/step !!!
      stepper->setAcceleration(15000);
      stepper->move(-1 * formula);
      currentAngle--;
      wireState = 0;
    }
    else if (wireState == 2002) {
      stepper->setSpeedInUs(250);       // the parameter is us/step !!!
      stepper->setAcceleration(15000);
      stepper->move(1 * formula);
      wireState = 0;
    }
    else if (wireState == 2003) {
      stepper->setSpeedInUs(250);       // the parameter is us/step !!!
      stepper->setAcceleration(15000);
      stepper->move(-1 * formula);
      wireState = 0;
    }
    else if (wireState == 2004) {
      stepper->setSpeedInUs(250);       // the parameter is us/step !!!
      stepper->setAcceleration(15000);
      stepper->move(450 * formula);
      wireState = 0;
    }
    else if (wireState == 2005) {
      stepper->setSpeedInUs(250);       // the parameter is us/step !!!
      stepper->setAcceleration(15000);
      stepper->move(-450 * formula);
      wireState = 0;
    }
    else if (wireState == 2006) {
      stepper->setSpeedInUs(2000);       // the parameter is us/step !!!
      stepper->setAcceleration(20000);
      stepper->move(1 * formula);
      wireState = 0;
    }
    else if (wireState == 2007) {
      stepper->setSpeedInUs(2000);       // the parameter is us/step !!!
      stepper->setAcceleration(20000);
      stepper->move(-1 * formula);
      wireState = 0;
    }
    else if (wireState > 0 && wireState < 2000) {
      newAngle = (wireState - currentAngle);
      stepper->setSpeedInUs(250);       // the parameter is us/step !!!
      stepper->setAcceleration(15000);
      stepper->move(newAngle * formula);  //Move X times revolutions, according to gear reduction ratio.
      currentAngle = wireState;
      wireState = 0;
    }
  }

}
