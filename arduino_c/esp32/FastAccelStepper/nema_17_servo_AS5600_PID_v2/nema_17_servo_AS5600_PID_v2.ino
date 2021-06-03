#include <Wire.h> //This is for i2C
#include <FastAccelStepper.h>
#include <PID_v1.h>

#define dirPinStepper_A    25
#define enablePinStepper_A 33
#define stepPinStepper_A  32  // OC1A in case of AVR

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepperA = NULL;
 
// PID stuffs
String readString; //This while store the user input data
int Raw_Input = 0;
int User_Input = 0; // This while convert input string into integer
int Last_User_Input = 0;

int lastEncoded = 0; // Here updated value of encoder store.
float encoderValue = 0; // Raw encoder value
float encoderOutput;

int enableThreshold = 6; // Minimum PID output to move. Higher value stops shaking while idle
int openSpeed = 250;
bool openLoopRunning = false;

int PPR = 4096;  // Encoder Pulse per revolution.
int motionAngle = 360; // Maximum degree of motion.
int REV = 0;          // Set point REQUIRED ENCODER VALUE

double kp = 6 , ki = 5 , kd = 0.01;
//double new_kp, new_ki, new_kd;
double input = 0, output = 0, setpoint = 0;
PID myPID(&input, &output, &setpoint, kp, ki, kd, DIRECT); 

// Stepper driver settings and gearboxes (if any)
float stepsPerRev = 200.0;
int microstepping = 4;
float formula = ((stepsPerRev * microstepping) / 360);
float gearReduction = 66.461538462; //EMC2 Gen 2 Gearbox

//---------------------------------------------------------------------------
//Magnetic sensor things
int magnetStatus = 0; //value of the status register (MD, ML, MH)

int lowbyte; //raw angle 7:0
word highbyte; //raw angle 7:0 and 11:8
int rawAngle; //final raw angle 
float degAngle; //raw angle in degrees (360/4096 * [value between 0-4095])

int quadrantNumber, previousquadrantNumber; //quadrant IDs
float numberofTurns = 0; //number of turns
float correctedAngle = 0; //tared angle - based on the startup value
float startAngle = 0; //starting angle
float totalAngle = 0; //total absolute angular displacement
float previoustotalAngle = 0; //for the display printing

void setup(){
  Serial.begin(115200); //start serial - tip: don't use serial if you don't need it (speed considerations)
  Wire.begin(); //start i2C  
  Wire.setClock(800000L); //fast clock

  checkMagnetPresence(); //check the magnet (blocks until magnet is found)

  ReadRawAngle(); //make a reading so the degAngle gets updated
  startAngle = degAngle; //update startAngle with degAngle - for taring

  myPID.SetMode(AUTOMATIC);   //set PID in Auto mode
  myPID.SetSampleTime(1);  // refresh rate of PID controller
  myPID.SetOutputLimits(-500, 500); // this is the MAX PWM value to move motor, here change in value reflect change in speed of motor.

  engine.init();
  stepperA = engine.stepperConnectToPin(stepPinStepper_A);
  if (stepperA) {
    stepperA->setDirectionPin(dirPinStepper_A);
    stepperA->setEnablePin(enablePinStepper_A);
    stepperA->setAutoEnable(true);

    stepperA->setSpeedInHz(500);       // the parameter is us/step !!!
    stepperA->setAcceleration(30000);
  }    
}

void loop(){    
  ReadRawAngle(); //ask the value from the sensor
  correctAngle(); //tare the value
  checkQuadrant(); //check quadrant, check rotations, check absolute angular position

  while (Serial.available()) { //Check if the serial data is available.
    delay(3);                  // a small delay
    char c = Serial.read();  // storing input data
    readString += c;         // accumulate each of the characters in readString
  }
 
  if (readString.length() >0) { //Verify that the variable contains information 
    if (readString[0] == 'm'){
      readString[0] = '0';

      //Check for negative numbers
      if(readString[1] == '-'){
        readString[1] = '0';
        Raw_Input = readString.toInt();   // here input data is store in integer form
        User_Input = -Raw_Input; 
      }else{
        User_Input = readString.toInt();   // here input data is store in integer form        
      }
      //Apply Gear Reduction
      User_Input = User_Input * gearReduction;
      
      //Print actual angle value     
      Serial.print("New position: ");
      Serial.println(User_Input);  //printing the input data in integer form
      readString=""; // Cleaning User input, ready for new Input  
      stepperOpenLoop(User_Input);
    }
    else if (readString[0] == 'p'){
      readString[0] = '0';
      Serial.print("New kP: ");
      Serial.println(readString.toDouble());  //printing the input data in integer form
      kp = readString.toDouble();   // here input data is store in integer form
      myPID.SetTunings(kp, ki, kd);
      readString=""; // Cleaning User input, ready for new Input  
    }
    else if (readString[0] == 'i'){
      readString[0] = '0';
      Serial.print("New kI: ");
      Serial.println(readString.toDouble());  //printing the input data in integer form
      ki = readString.toDouble();   // here input data is store in integer form
      myPID.SetTunings(kp, ki, kd);
      readString=""; // Cleaning User input, ready for new Input  
    }
    else if (readString[0] == 'd'){
      readString[0] = '0';
      Serial.print("New kD: ");
      Serial.println(readString.toDouble());  //printing the input data in integer form
      kd = readString.toDouble();   // here input data is store in integer form
      myPID.SetTunings(kp, ki, kd);
      readString=""; // Cleaning User input, ready for new Input  
    }   
    else if (readString[0] == 'a'){
      Serial.print("PID values and Angle: P");
      Serial.print(kp);  //printing the input data in integer form
      Serial.print(", I");      
      Serial.print(ki);  //printing the input data in integer form
      Serial.print(", D");        
      Serial.print(kd);  //printing the input data in integer form
      Serial.print(", M");    
      Serial.print(User_Input);     
      Serial.print(", Enc: ");    
      Serial.print(totalAngle); 
      Serial.print(", Out: ");    
      Serial.print(output);
      Serial.print(", Open: ");
      if(openLoopRunning == true){
        Serial.println("yes");        
      }else{
        Serial.println("no");      
      }
      readString=""; // Cleaning User input, ready for new Input                              
    }           
  }

  //Check if stepper is running to switch open loop to closed loop
  if(stepperA->isRunning() == false){
    openLoopRunning = false;  
  }

  // Switch to closed loop
  if(openLoopRunning == false){
    setpoint = User_Input;                    //PID while work to achive this value consider as SET value
    input = totalAngle;           // data from encoder consider as a Process value
    myPID.Compute();                 // calculate new output    
    stepperClosedLoop(output);  
  } 
}

void ReadRawAngle(){ 
  //7:0 - bits
  Wire.beginTransmission(0x36); //connect to the sensor
  Wire.write(0x0D); //figure 21 - register map: Raw angle (7:0)
  Wire.endTransmission(); //end transmission
  Wire.requestFrom(0x36, 1); //request from the sensor
  
  while(Wire.available() == 0); //wait until it becomes available 
  lowbyte = Wire.read(); //Reading the data after the request
 
  //11:8 - 4 bits
  Wire.beginTransmission(0x36);
  Wire.write(0x0C); //figure 21 - register map: Raw angle (11:8)
  Wire.endTransmission();
  Wire.requestFrom(0x36, 1);
  
  while(Wire.available() == 0);  
  highbyte = Wire.read();
  
  //4 bits have to be shifted to its proper place as we want to build a 12-bit number
  highbyte = highbyte << 8; //shifting to left
  rawAngle = highbyte | lowbyte; //int is 16 bits (as well as the word)
  degAngle = rawAngle * 0.087890625; 
  
  //Serial.print("Deg angle: ");
  //Serial.println(degAngle, 2); //absolute position of the encoder within the 0-360 circle
  
}

void correctAngle(){
  //recalculate angle
  correctedAngle = degAngle - startAngle; //this tares the position

  if(correctedAngle < 0){ //if the calculated angle is negative, we need to "normalize" it
    correctedAngle = correctedAngle + 360; //correction for negative numbers (i.e. -15 becomes +345)
  }
  else{}
  //Serial.print("Corrected angle: ");
  //Serial.println(correctedAngle, 2); //print the corrected/tared angle  
}

void checkQuadrant(){
  //Quadrant 1
  if(correctedAngle >= 0 && correctedAngle <=90){
    quadrantNumber = 1;
  }

  //Quadrant 2
  if(correctedAngle > 90 && correctedAngle <=180){
    quadrantNumber = 2;
  }

  //Quadrant 3
  if(correctedAngle > 180 && correctedAngle <=270){
    quadrantNumber = 3;
  }

  //Quadrant 4
  if(correctedAngle > 270 && correctedAngle <360){
    quadrantNumber = 4;
  }
  //Serial.print("Quadrant: ");
  //Serial.println(quadrantNumber); //print our position "quadrant-wise"

  if(quadrantNumber != previousquadrantNumber){ //if we changed quadrant
    if(quadrantNumber == 1 && previousquadrantNumber == 4){
      numberofTurns++; // 4 --> 1 transition: CW rotation
    }

    if(quadrantNumber == 4 && previousquadrantNumber == 1){
      numberofTurns--; // 1 --> 4 transition: CCW rotation
    }
    //this could be done between every quadrants so one can count every 1/4th of transition

    previousquadrantNumber = quadrantNumber;  //update to the current quadrant
  
  }  
  //Serial.print("Turns: ");
  //Serial.println(numberofTurns,0); //number of turns in absolute terms (can be negative which indicates CCW turns)  

  //after we have the corrected angle and the turns, we can calculate the total absolute position
  totalAngle = (numberofTurns*360) + correctedAngle; //number of turns (+/-) plus the actual angle within the 0-360 range

  //Serial.print("Total angle: ");
  //Serial.println(totalAngle, 2); //absolute position of the motor expressed in degree angles, 2 digits
}

void checkMagnetPresence(){  
  //This function runs in the setup() and it locks the MCU until the magnet is not positioned properly

  while((magnetStatus & 32) != 32){ //while the magnet is not adjusted to the proper distance - 32: MD = 1
    magnetStatus = 0; //reset reading

    Wire.beginTransmission(0x36); //connect to the sensor
    Wire.write(0x0B); //figure 21 - register map: Status: MD ML MH
    Wire.endTransmission(); //end transmission
    Wire.requestFrom(0x36, 1); //request from the sensor

    while(Wire.available() == 0); //wait until it becomes available 
    magnetStatus = Wire.read(); //Reading the data after the request    
  }      
}

void stepperClosedLoop(int out) {                              
  if (abs(out) < enableThreshold){
    stepperA->stopMove();  
  }else{
    if (out > 0) {
      stepperA->setSpeedInHz(abs(out));
      stepperA->applySpeedAcceleration();   
      stepperA->runForward();
    }
    else if (out < 0) {
      stepperA->setSpeedInHz(abs(out));
      stepperA->applySpeedAcceleration();    
      stepperA->runBackward();
    }  
  }
}

void stepperOpenLoop(float openSteps){
  int actualSteps = (openSteps - Last_User_Input) * formula;

  // Set open loop running flag
  openLoopRunning = true;

  //Serial.println(actualSteps);
  //Serial.println(formula);

  // Open loop runs faster than closed loop error correction
  stepperA->setSpeedInUs(openSpeed);
  stepperA->setAcceleration(25000);  
  stepperA->applySpeedAcceleration();
  stepperA->move(actualSteps);
  
  Last_User_Input = openSteps;
}
