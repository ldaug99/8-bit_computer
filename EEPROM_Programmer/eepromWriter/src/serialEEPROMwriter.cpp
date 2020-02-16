#include <Arduino.h>
#include "serialEEPROMwriter.h"
//************************************************************************************
// Public functions
//************************************************************************************
// Setup pinout
serialEEPROMwriter::serialEEPROMwriter() {
    setupHW();
}
// Start seiral communication
void serialEEPROMwriter::begin(uint32_t baudRate = defaultBaudRate) {
    setupSerial(baudRate);
}
// Read from serial
void serialEEPROMwriter::readSerial() {
    String input = readFromSerial();
    if (input != "null") {
        processInput(input);
    }
}
// End serial communication
void serialEEPROMwriter::end() {
    Serial.end();
}
//************************************************************************************
// Private functions
//************************************************************************************
// Write address and data to serial prompt
void serialEEPROMwriter::writeToSerial(uint16_t address, uint8_t data) {
    Serial.print(address);
    Serial.print(",");
    Serial.println(data); // Prints data and \n character
    Serial.flush();
}
// Pulse write
void serialEEPROMwriter::pulseWrite() {
    digitalWrite(EW, LOW);
    delayMicroseconds(pulseTime); // Wrtie pulse should be 100 ns, function works accurately down to 3 micro seconds
    digitalWrite(EW, HIGH);
    delayMicroseconds(pinDelay);
}
// Set data
void serialEEPROMwriter::setData(uint8_t data) {
    for (uint8_t i = 0; i < EEPROM_pins; i ++) {
        digitalWrite(EEPROM_pin[i], bitRead(data, i));
    }
    delayMicroseconds(pinDelay);
}
// Write to EEPROM
void serialEEPROMwriter::writeEEPROM(uint16_t address, uint8_t data) {
    shiftOutAddress(address);
    setEEPROM(OUTPUT);
    setData(data);
    pulseWrite();
    setEEPROM(INPUT);
}
// Get data
uint8_t serialEEPROMwriter::getData() {
    uint8_t data = 0;
    for (uint8_t i = 0; i < EEPROM_pins; i ++) {
        data = data + (digitalRead(EEPROM_pin[i]) << i);
    }
    return data;
}
// Read from EEPROM
uint8_t serialEEPROMwriter::readEEPROM(uint16_t address) {
    shiftOutAddress(address);
    setEEPROM(INPUT);
    return getData();
}
// Shift out address to 74HC164
void serialEEPROMwriter::shiftOutAddress(uint16_t address) {
    byte lb_addr = (byte) address;
    byte hb_addr = (byte) (address >> 8);
    shiftOut(SO, SC, MSBFIRST, hb_addr);
    shiftOut(SO, SC, MSBFIRST, lb_addr);
}

// Process serial command
void serialEEPROMwriter::processInput(String input) {
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
// Read from Serial
String serialEEPROMwriter::readFromSerial() {
    if (Serial.available() > 0) {
        return Serial.readStringUntil('\n');
    }
    return "null";
}
// Setup serial connection
void serialEEPROMwriter::setupSerial(uint32_t baudRate) {
    Serial.begin(baudRate);
    Serial.print("EEPROM programmer started at baud rate ");
    Serial.println(String(baudRate));
    Serial.flush();
}
// Setup 74HC164 out and clock pin
void serialEEPROMwriter::setupShift() {
    digitalWrite(SO, LOW);
    pinMode(SO, OUTPUT);
    digitalWrite(SC, LOW);
    pinMode(SC, OUTPUT);
    shiftOut(SO, SC, MSBFIRST, 0);
    shiftOut(SO, SC, MSBFIRST, 0);
}
// Set data pins mode for EEPROM, input or output (read or write data)
void serialEEPROMwriter::setEEPROM(uint8_t mode) {
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
// Setup EEPROM read and write pins
void serialEEPROMwriter::setupEEPROM() {
    pinMode(ER, OUTPUT);
    digitalWrite(ER, LOW);
    digitalWrite(EW, HIGH);
    pinMode(EW, OUTPUT);
    digitalWrite(CE, LOW);
    pinMode(CE, OUTPUT);
    setEEPROM(INPUT);
}
// Setup EEPROM and 74HC164
void serialEEPROMwriter::setupHW() {
    setupEEPROM();
    setupShift();
}