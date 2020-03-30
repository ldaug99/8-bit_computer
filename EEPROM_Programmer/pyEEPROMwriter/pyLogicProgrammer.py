from pyEEPROMwriter import pyEEPROM
import pyCSVloader

def strArrayBinToDec(arrayBin, invert = False):
    # Convert an string array of binary numbers to a decimal number 
    forRange = range(0, len(arrayBin))
    if invert:
        forRange = range(len(arrayBin), 0, -1)
    strBin = ""
    for i in forRange:
        strBin = strBin + arrayBin[i - 1] 
    print(arrayBin)
    print(strBin)
    return strBinToDec(strBin)

def strBinToDec(strBin):
    # Convert a binary number (as string) to a deicmal number
    # MSB is left most bit
    # Input example: "1101001", Output: 105
    dec = 0 # Initialize decimal number as 0
    binLength = len(strBin) # Get length of binary number (number of bits)
    for i in range(binLength,0,-1): # Loop through each bit, starting from MSB (left most, highes index)
        power = (i - 1) # Get power to 
        bit = int(strBin[binLength - i]) # Get bit from binary number (1 or 0)
        dec = dec + bit * (2 ** power) # Add number fro bit to deciaml if bit is 1
    return dec


data = pyCSVloader.loadCSV("logic.txt")

# From 1 to 4
eepromNr = 4
eepromData = pyCSVloader.splitToEEPROM(eepromNr, data)

trueData = [[],[]]
for i in range(0, len(eepromData[0])):
    trueData[0].append(strArrayBinToDec(eepromData[0][i], True))
    trueData[1].append(strArrayBinToDec(eepromData[1][i], True))
    print("Addr: {}, data: {}".format(trueData[0][i], trueData[1][i]))


promWriter = pyEEPROM("COM4", 115200)
failedWrite, failedVerify = promWriter.writeArray(trueData[0], trueData[1])

print("Failed to write: {}".format(failedWrite))
print("Failed to verify: {}".format(failedVerify))

promWriter.close()

