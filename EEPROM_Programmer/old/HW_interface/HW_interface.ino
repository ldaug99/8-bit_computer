//************************************************************************************
// Include libraries
#include <Arduino.h>
//************************************************************************************
//
#define defaultBaudRate 115200
#define ED0 4
#define ED1 5
#define ED2 6
#define ED3 7
#define ED4 8
#define ED5 9
#define ED6 10
#define ED7 11
#define EEPROM_pins 8
#define ER A5
#define EW A4
#define CE A3
// Serial shift definitions
#define SO 3
#define SC 2
#define pulseTime 5 // Write pulse should be 100 ns, function works accurately down to 3 micro seconds
#define pinDelay 3
//************************************************************************************
// Global variables
const uint8_t EEPROM_pin[EEPROM_pins] = {ED0, ED1, ED2, ED3, ED4, ED5, ED6, ED7};
uint8_t EEPROM_mode;
//************************************************************************************
// Functions
//
void setupSerial(uint32_t baudRate = defaultBaudRate) {
    Serial.begin(baudRate);
    Serial.print("EEPROM programmer started at baud rate ");
    Serial.println(String(baudRate));
    Serial.flush();
}
// Read from Serial
String readFromSerial() {
    if (Serial.available() > 0) {
        return Serial.readStringUntil('\n');
    }
    return "null";
}
// Process serial command
void processInput(String input) {
    int16_t LFindex = input.indexOf('\n');
    if (LFindex > 0) {
        input = input.substring(0, LFindex);
    }
    int16_t SEPindex = input.indexOf(",");
    if (SEPindex > 0) { // Write command
        uint16_t address = (uint16_t) (input.substring(0, SEPindex)).toInt();
        uint8_t data = (uint8_t) (input.substring(SEPindex + 1)).toInt();
        writeEEPROM(address, data);
        Serial.println("OK");
    } else { // Read command
        uint16_t address = (uint16_t) input.toInt();
        uint8_t data = readEEPROM(address);
        writeToSerial(address, data);
    }
}
// Write address and data to serial prompt
void writeToSerial(uint16_t address, uint8_t data) {
    Serial.print(address);
    Serial.print(",");
    Serial.println(data); // Prints data and \n character
    Serial.flush();
}
// Read from EEPROM
uint8_t readEEPROM(uint16_t address) {
    shiftOutAddress(address);
    setEEPROM(INPUT);
    return getData();
}
// Write to EEPROM
void writeEEPROM(uint16_t address, uint8_t data) {
    shiftOutAddress(address);
    setEEPROM(OUTPUT);
    setData(data);
    pulseWrite();
    setEEPROM(INPUT);
}
// Pulse write
void pulseWrite() {
    digitalWrite(EW, LOW);
    delayMicroseconds(pulseTime); // Wrtie pulse should be 100 ns, function works accurately down to 3 micro seconds
    digitalWrite(EW, HIGH);
    delayMicroseconds(pinDelay);
}
// Set data
void setData(uint8_t data) {
    for (uint8_t i = 0; i < EEPROM_pins; i ++) {
        digitalWrite(EEPROM_pin[i], bitRead(data, i));
    }
    delayMicroseconds(pinDelay);
}
// Get data
uint8_t getData() {
    uint8_t data = 0;
    for (uint8_t i = 0; i < EEPROM_pins; i ++) {
        data = data + (digitalRead(EEPROM_pin[i]) << i);
    }
    return data;
}
// Setup EEPROM and 74HC164
void setupHW() {
    setupEEPROM();
    setupShift();
}
// Setup EEPROM read and write pins
void setupEEPROM() {
    pinMode(ER, OUTPUT);
    digitalWrite(ER, LOW);
    digitalWrite(EW, HIGH);
    pinMode(EW, OUTPUT);
    digitalWrite(CE, LOW);
    pinMode(CE, OUTPUT);
    setEEPROM(INPUT);
}
// Setup 74HC164 out and clock pin
void setupShift() {
    digitalWrite(SO, LOW);
    pinMode(SO, OUTPUT);
    digitalWrite(SC, LOW);
    pinMode(SC, OUTPUT);
    shiftOut(SO, SC, MSBFIRST, 0);
    shiftOut(SO, SC, MSBFIRST, 0);
}
// Set data pins mode for EEPROM, input or output (read or write data)
void setEEPROM(uint8_t mode) {
    if (EEPROM_mode != mode) {
        EEPROM_mode = mode;
        if (mode == OUTPUT) {
            digitalWrite(ER, HIGH);
        } else {
            digitalWrite(ER, LOW);
        }
        for (uint8_t i = 0; i < EEPROM_pins; i++) {
            pinMode(EEPROM_pin[i], mode);
        }
    }
    delayMicroseconds(pinDelay);
}
// Shift out address to 74HC164
void shiftOutAddress(uint16_t address) {
    byte lb_addr = (byte) address;
    byte hb_addr = (byte) (address >> 8);
    shiftOut(SO, SC, MSBFIRST, hb_addr);
    shiftOut(SO, SC, MSBFIRST, lb_addr);
}
//************************************************************************************
// Setup
void setup() {
    setupHW();
    setupSerial();
}
//************************************************************************************
// Main loop
void loop() {
    String input = readFromSerial();
    if (input != "null") {
        processInput(input);
    }
}
//************************************************************************************