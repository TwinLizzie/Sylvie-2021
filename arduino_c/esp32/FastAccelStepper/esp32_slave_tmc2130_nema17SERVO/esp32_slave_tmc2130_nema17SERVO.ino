#define EN_PIN    33  // Nano v3:   16 Mega:    38  //enable (CFG6)
#define DIR_PIN   25  //            19          55  //direction
#define STEP_PIN  32  //            18          54  //step
#define CS_PIN    5  //            17          40  //chip select
#define R_SENSE 0.11f // Match to your driver

#define SDA_PIN 2
#define SCL_PIN 4

#define ANALOG_PIN 35

#define I2C_SLAVE_ADDR 0x60

#include <TMCStepper.h>
TMC2130Stepper driver = TMC2130Stepper(CS_PIN, R_SENSE); // Hardware SPI

#include <FastAccelStepper.h>
FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepperA = NULL;

#include <Wire.h>
#include <WireSlave.h>
#include <PID_v1.h>

// Wire character read stuffs
int Raw_Input = 0;
int User_Input = 0; // This while convert input string into integer
int potValue = 0;

boolean flagRx = false;
char readStringC[10]; //This while store the user input data

// PID stuffs
double kp = 6 , ki = 5 , kd = 0.01;
//double new_kp, new_ki, new_kd;
double input = 0, output = 0, setpoint = 0;
PID myPID(&input, &output, &setpoint, kp, ki, kd, DIRECT); 

// Motor and driver speed stuffs
long closedSpeed = 20;
long openSpeed = 10; // Less is more
long openAccel = 400000;
int enableThreshold = 6;

bool openLoopRunning = false;
bool closedLoopRunning = true;

// Encoder stuffs
long revolutions = 0;   // number of revolutions the encoder has made
double encoderPosition = 0;    // the calculated value the encoder is at
double totalAngle;
double encoderOutput;          // raw value from AS5600
double firstEncoderOutput;
long lastEncoderOutput;        // last output from AS5600

// Stepper driver settings and gearboxes (if any)
float stepsPerRev = 200.0;
int microstepping = 32;
float formula = ((stepsPerRev * microstepping) / 360);
float gearReduction = 66.461538462; //EMC2 Gen 2 Gearbox

long driverCurrent = 1000;

//Refresh rate of the encoder
unsigned long previousMillis = 0;        // will store last time LED was updated
const long interval = 200;           // interval at which to blink (milliseconds)

void setup() {
  Serial.begin(115200);
  SPI.begin();
  
  bool success = WireSlave.begin(SDA_PIN, SCL_PIN, I2C_SLAVE_ADDR);
  if (!success) {
    Serial.println("I2C slave init failed");
    while(1) delay(100);
  }
  else {
    Serial.println("I2C slave init success!"); 
  }
  WireSlave.onReceive(receiveEvent);

  myPID.SetMode(AUTOMATIC);   //set PID in Auto mode
  myPID.SetSampleTime(1);  // refresh rate of PID controller
  myPID.SetOutputLimits(-500, 500); // this is the MAX PWM value to move motor, here change in value reflect change in speed of motor.
  
  engine.init();
  stepperA = engine.stepperConnectToPin(STEP_PIN);
  if (stepperA) {
    stepperA->setDirectionPin(DIR_PIN);
    stepperA->setEnablePin(EN_PIN);
    stepperA->setAutoEnable(true);

    stepperA->setSpeedInUs(openSpeed);       // the parameter is us/step !!!
    stepperA->setAcceleration(openAccel);
  }

  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);
  driver.begin();             // Initiate pins and registeries
  driver.rms_current(driverCurrent);    // Set stepper current to 600mA. The command is the same as command TMC2130.setCurrent(600, 0.11, 0.5);
  driver.microsteps(microstepping);
  driver.shaft(true);

  firstEncoderOutput = analogRead(ANALOG_PIN);
  encoderOutput = firstEncoderOutput;
  lastEncoderOutput = firstEncoderOutput;
  encoderPosition = firstEncoderOutput;
}

void getEncoderReading() {
  encoderOutput = analogRead(ANALOG_PIN);           // get the raw value of the encoder                      
  
  if ((lastEncoderOutput - encoderOutput) > 2047 )        // check if a full rotation has been made
    revolutions++;
  else if ((lastEncoderOutput - encoderOutput) < -2047 )
    revolutions--;
    
  encoderPosition = (revolutions * 4096 + encoderOutput) - firstEncoderOutput;   // calculate the position the the encoder is at based off of the number of revolutions
  totalAngle = (encoderPosition * (360.0 / 4096.0)); // The Value that Matters
  
  //Serial.println(totalAngle);
  
  lastEncoderOutput = encoderOutput;   
}


void stepperClosedLoop(int out) {                              
  if (abs(out) < enableThreshold){
    stepperA->stopMove(); 
    closedLoopRunning = false;
  }else{
    if (out > 0) {
      int newSpeed = map(abs(out), 0, 500, 1000, closedSpeed);
      stepperA->setSpeedInUs(newSpeed);
      stepperA->applySpeedAcceleration();   
      stepperA->runForward();
    }
    else if (out < 0) {
      int newSpeed = map(abs(out), 0, 500, 1000, closedSpeed);      
      stepperA->setSpeedInUs(newSpeed);
      stepperA->applySpeedAcceleration();    
      stepperA->runBackward();
    }  
  }
}

void stepperOpenLoop(float openSteps){
  int actualSteps_relative = openSteps * formula;
  int actualAngle = totalAngle * formula;

  openLoopRunning = true;
  closedLoopRunning = true;

  stepperA->setCurrentPosition(actualAngle);  

  // Open loop runs faster than closed loop error correction
  stepperA->setSpeedInUs(openSpeed);
  stepperA->setAcceleration(openAccel);  
  stepperA->applySpeedAcceleration();
  stepperA->moveTo(actualSteps_relative);
}

void receiveEvent(int byteCount) {
  int i;
  for (i = 0; i < byteCount; i++)
  {
    readStringC[i] = WireSlave.read();     // receive byte as a character
  }
  readStringC[i] = '\0';  // assume it is a string, add zero-terminator
  flagRx = true;    // set flag, we received something.
}

void loop() {
  WireSlave.update();
  getEncoderReading();
 
  if (flagRx == true) { //Verify that the variable contains information 
    if (readStringC[0] == 'm'){
      readStringC[0] = '0';

      //Check for negative numbers
      if(readStringC[1] == '-'){
        readStringC[1] = '0';
        Raw_Input = atoi(readStringC);   // here input data is store in integer form
        User_Input = -Raw_Input; 
      }else{
        User_Input = atoi(readStringC);   // here input data is store in integer form   
      }
      //Apply Gear Reduction
      int Display_Input = User_Input;
      User_Input = User_Input * gearReduction;
      
      //Print actual angle value          
      stepperOpenLoop(User_Input);
    }
    else if (readStringC[0] == 's'){
      readStringC[0] = '0';
      openSpeed = atoi(readStringC); 
    }
    else if (readStringC[0] == 'c'){
      readStringC[0] = '0';
      if(atoi(readStringC) <= 1200){
        driverCurrent = atoi(readStringC);
        driver.rms_current(driverCurrent); 
      }
    }
    flagRx = false;
  }

  if (stepperA->isRunning() == false){
    openLoopRunning = false;  
  }

  if(openLoopRunning == false){
    if(closedLoopRunning == true){
      setpoint = User_Input;                    //PID while work to achive this value consider as SET value
      input = totalAngle;           // data from encoder consider as a Process value
      myPID.Compute();                 // calculate new output       
      stepperClosedLoop(output);    
    }       
  }
}
