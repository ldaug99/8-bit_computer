//************************************************************************************
// Include libraries
#include <Arduino.h>
//************************************************************************************
// Control line pinout
#define RESET 6 // Master reset, active HIGH
#define CLOCK 5 // Override clock, active HIGH
#define CDIS 7 // Control logic disable, active HIGH
#define BOUT 8 // BUS out, active LOW
#define HLT 9 // Halt clock, stop computer
// Serial shift definitions
#define SO 4 // Serial out
#define SC 3 // Serial clock
// Button pinout
#define PROG 2 // Program button
// Computer data bitness
#define dataBitLevel uint8_t
// Computer address bitness
#define addressBitLevel uint8_t

const static uint8_t ramTypeLocation = 0;
const static uint8_t addressLocation = 5;
const static uint8_t data0Location = 11;
const static uint8_t data1Location = 17;
const static uint8_t data2Location = 23;
const static uint8_t data3Location = 29;

const static uint8_t addressLength = 2;
const static uint8_t dataLength = 2;

const static uint8_t decCharI = 105; // Char i is 105 decimal
const static uint8_t decCharD = 100; // Char d is 100 decimal
/* 
* Shift 1
* QA => B0
* QB => B1
* QC => B2
* QD => B3
* QE => B4
* QF => B5
* DG => B6
* DH => B7
* Shift 2
* QA => IR
* QB => II
* QC => IA
* QD => IB
* QE => DR
* QF => DI
* DG => DA
* DH => DB
* Decimal to save to instruction address register: 1, bin 00000001
* Decimal to save to instruction memory: 2, bin 00000010
* Decimal to save to instruction memory alt 1: 6, bin 00000110
* Decimal to save to instruction memory alt 2: 10, bin 00001010
* Decimal to save to instruction memory alt 3: 14, bin 00001110
* Decimal to save to data address register: 16, bin 00010000
* Decimal to save to data memory: 32, bin 00100000
* Decimal to save to data memory alt 1: 96, bin 01100000
* Decimal to save to data memory alt 2: 160, bin 10100000
* Decimal to save to data memory alt 3: 224, bin 11100000
*/
const static uint8_t iAddr = 1;
const static uint8_t iData0 = 2;
const static uint8_t iData1 = 6;
const static uint8_t iData2 = 10;
const static uint8_t iData3 = 14;
const static uint8_t dAddr = 16;
const static uint8_t dData0 = 32;
const static uint8_t dData1 = 96;
const static uint8_t dData2 = 160;
const static uint8_t dData3 = 224;

const static uint8_t memLocations = 2;
const static uint8_t lineSteps = 5;

const static uint8_t controlLines[memLocations][lineSteps] = {
  {iAddr, iData0, iData1, iData2, iData3},
  {dAddr, dData0, dData1, dData2, dData3}
};
//************************************************************************************
// Global variables
bool doProgram = false;
//************************************************************************************
// Functions
// Interrupt handler
void startProg() {
  detachInterrupt(digitalPinToInterrupt(PROG));
  doProgram = true;
}
// Setup pinout
void setupPinout() {
  // Serial out
  pinMode(SO, OUTPUT);
  pinMode(SC, OUTPUT);
  // Button
  pinMode(PROG, INPUT);
  // Control lines
  pinMode(RESET, OUTPUT);
  pinMode(CLOCK, OUTPUT);
  pinMode(CDIS, OUTPUT);
  digitalWrite(BOUT, HIGH); // Active low
  pinMode(BOUT, OUTPUT);
  pinMode(HLT, OUTPUT);
  // Attach button interrupt
  attachInterrupt(digitalPinToInterrupt(PROG), startProg, RISING);
}
// Convert hex to decimal
uint8_t hexToDecimal(uint8_t hex, uint8_t position) {
  uint8_t sum = 0;
  switch (hex) {
    case 48 ... 57:
      sum = hex - 48;
    break;
    case 65 ... 70:
      sum = (hex - 65) + 10; // 65 is char A, in HEX A = 10, thus + 10
    break;
    default:
      sum = 0;
    break;
  }
  sum = sum << ((position - 1) * 4);
  return sum;
}
// Convert part of string to decimal value
uint8_t getDecimalFromHEXString(String input, uint8_t startLocation, uint8_t length) {
  uint8_t decimal = 0;
  Serial.print("DecToHex got input string: ");
  Serial.println(input);
  for (uint8_t i = 0; i < length; i++) {
    decimal = decimal + hexToDecimal(input[startLocation + i], length - i);
  }
  return decimal;
}
// Get ram location (instruction or data)
uint8_t getRamLocation(uint8_t ramType) {
    if (ramType == decCharI) { 
      return 0; // Save to instruction memory
    } else if (ramType == decCharD) { 
      return 1; // Save to data memory
    } else { // Invalid type...
      for (;;) {
        // Imma stop you right there...
      }
    }
}
// Pulse clock
void pulseClock() {
  digitalWrite(CLOCK, HIGH);
  delay(10);
  digitalWrite(CLOCK, LOW);
}
// Set data and control
void shiftOutAndSet(uint8_t data, uint8_t control) {
  // Shift out data
  Serial.print("Setting data. BIN: ");
  Serial.print(data, BIN);
  Serial.print(" HEX: ");
  Serial.println(data, HEX);
  shiftOut(SO, SC, MSBFIRST, control); // Control signal
  shiftOut(SO, SC, MSBFIRST, data); // Bus data
  delay(100);
  // Pulse clock
  pulseClock();
}
// Stop computer
void haltComputer() {
  digitalWrite(CDIS, HIGH); // Disable control logic
  digitalWrite(HLT, HIGH); // Stop clock
  digitalWrite(RESET, HIGH); // Pulse reset
  delay(100);
  digitalWrite(RESET, LOW);
  digitalWrite(BOUT, LOW); // Enable output to computer bus from shift registers
}
// Start computer
void startComputer() {
  shiftOut(SO, SC, MSBFIRST, 0); // Control signal
  shiftOut(SO, SC, MSBFIRST, 0); // Bus data
  digitalWrite(BOUT, HIGH); // Disable output to computer bus from shift registers
  digitalWrite(RESET, HIGH); // Pulse reset
  delay(100);
  digitalWrite(RESET, LOW);
  digitalWrite(HLT, LOW); // Release halt signal
  digitalWrite(CDIS, LOW); // Enable control logic
}
// Get address and data for each line of program data
void programComputer(String input) {
  Serial.print("Programming line: ");
  Serial.println(input);
  uint8_t programLine[lineSteps + 1];
  programLine[0] = getRamLocation((uint8_t)input[0]);
  programLine[1] = getDecimalFromHEXString(input, addressLocation, addressLength);
  programLine[2] = getDecimalFromHEXString(input, data0Location, dataLength);
  programLine[3] = getDecimalFromHEXString(input, data1Location, dataLength);
  programLine[4] = getDecimalFromHEXString(input, data2Location, dataLength);
  programLine[5] = getDecimalFromHEXString(input, data3Location, dataLength);
  for (uint8_t k = 0; k < lineSteps; k++) {
    shiftOutAndSet(programLine[k + 1], controlLines[programLine[0]][k]);
    delay(10);
  }
}
//************************************************************************************
// Setup
void setup() {
  Serial.begin(115200);
  setupPinout();
  shiftOut(SO, SC, MSBFIRST, 0); // Control signal
  shiftOut(SO, SC, MSBFIRST, 0); // Bus data
}
//************************************************************************************
// Main loop
void loop() {
  if (doProgram) {
    Serial.println("Starting programming computer. Read to receive data.");
    haltComputer();
    uint8_t waitForSerial = true;
    while(waitForSerial) {
      if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        if (input.indexOf("Done") >= 0) {
          waitForSerial = false;
        } else if (input.indexOf("d") >= 0 || input.indexOf("i") >= 0) {
          programComputer(input);
          Serial.println("OK");
        }
      }
    }
    doProgram = false;
    startComputer();
    attachInterrupt(digitalPinToInterrupt(PROG), startProg, RISING);
    Serial.println("Done programming computer");
  }
}
//************************************************************************************