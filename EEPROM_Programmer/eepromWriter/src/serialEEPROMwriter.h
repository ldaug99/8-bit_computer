
// Simple serial EEPROM reader/writer
// To shift register are used to set address
// Data is read using digital pins
// Global definitions
// EEPROM pinout
#define defaultBaudRate 250000
#define ED0 4 // EEPROM data pins, ED0 = I/O0 on EEPROM
#define ED1 5
#define ED2 6
#define ED3 7
#define ED4 8
#define ED5 9
#define ED6 10
#define ED7 11
#define EEPROM_pins 8
#define ER A5 // EEPROM read enable
#define EW A4 // EEPROM write enable
#define CE A3 // EEPROM chip enable
// Serial shift definitions
#define SO 3 // Shift out
#define SC 2 // Shift clock
#define pulseTime 5 // Write pulse should be 100 ns, function works accurately down to 3 micro seconds
#define pinDelay 3
// ensure this library description is only included once
#ifndef serialEEPROMwriter_h
#define serialEEPROMwriter_h
// Include Arduino
#include <Arduino.h>
// Class
class serialEEPROMwriter {
    public:
        // Class initializer
        serialEEPROMwriter();

        void begin(uint32_t baudRate = defaultBaudRate); // Setup serial and EEPROM
        void readSerial(); // Run in loop to read from serial and write/read to EEPROM
        void end();

    private:
        const uint8_t EEPROM_pin[EEPROM_pins] = {ED0, ED1, ED2, ED3, ED4, ED5, ED6, ED7};
        uint8_t EEPROM_mode;

        void setupHW();
        void setupEEPROM();
        void setupShift();
        void setupSerial(uint32_t baudRate);

        void setEEPROM(uint8_t mode);
        uint8_t readEEPROM(uint16_t address);
        void writeEEPROM(uint16_t address, uint8_t data);
        void setData(uint8_t data);
        uint8_t getData();
        void shiftOutAddress(uint16_t address);
        void pulseWrite();

        void writeToSerial(uint16_t address, uint8_t data);
        void processInput(String input);
        String readFromSerial();
};
#endif