Syntax:
"ramType, address, data0, data1, data2, data3"

ramType: Can be d for data ram or i for instruction ram.
address: RAM address.
data1: Data on address.
data2: Data on address + Alternet 1.
data3: Data on address + Alternet 2.
data4: Data on address + Alternet 1 and 2.

When ramType is i, data1 is opcode of command

Example op line in program file:
"d, 0x00, 0xFF, 0x00, 0x00, 0x00"

Each line is ended by a , except for the last line