#include <Arduino.h> 
const static uint8_t programLength = 8; 
const static uint8_t lineParts = 6; 
const static uint8_t programData[programLength][lineParts] = { 
    {100, 0, 1, 0, 0, 0},
    {100, 1, 2, 0, 0, 0},
    {105, 0, 2, 0, 0, 0},
    {105, 1, 3, 1, 0, 0},
    {105, 2, 252, 3, 0, 0},
    {105, 3, 4, 0, 0, 0},
    {105, 4, 250, 0, 0, 0},
    {105, 5, 252, 3, 0, 0} 
}; 
