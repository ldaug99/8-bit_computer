# Simple functions for converting between number systems

binToHex = {
    "0000": "0", "0001": "1", "0010": "2", "0011": "3",
    "0100": "4", "0101": "5", "0110": "6", "0111": "7",
    "1000": "8", "1001": "9", "1010": "A", "1011": "B",
    "1100": "C", "1101": "D", "1110": "E", "1111": "F"
}

hexToBin = {
    "0": "0000", "1": "0001", "2": "0010", "3": "0011",
    "4": "0100", "5": "0101", "6": "0110", "7": "0111",
    "8": "1000", "9": "1001", "A": "1010", "B": "1011",
    "C": "1100", "D": "1101", "E": "1110", "F": "1111"
}

decToHex = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
    8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"
}

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

def decToStrHex(dec):
    # Convert a decimal number to a hexadecimal number (as string, with 0x)
    # MSB is left most bit
    # Input example: 105, Output: "0x69"
    hexNum = ""
    base = 16 # Hexadeicmal base
    quotient = dec
    while (quotient > 0):
        remainder = quotient % base # Get reminder from division with base
        quotient = int(quotient / base) # Devide with 
        hexNum = decToHex[remainder] + hexNum
    hexNum = "0x" + hexNum # Add "0x"
    return hexNum

def strDecToHex(strDec):
    dec = int(strDec) # Convert string to int
    hexNum = decToStrHex(dec) # Convert decimal humber to hexadecimal number
    return hexNum

def strBinToStrHex(strBin):
    # Convert a binary number (as string) to a hexadecimal number (as string, with 0x)
    # MSB is left most bit
    # Input example: "1101001", Output: "0x69"
    dec = strBinToDec(strBin) # Convert binary number to decimal number
    hexNum = decToStrHex(dec) # Convert decimal number ot hex
    return hexNum

def strHexToDec(strHex):
    # Convert a hexadeicmal number (with 0x) to a decimal number
    strHex = strHex[2::]
    binary = ""
    for i in range(0, len(strHex)):
        binary = binary + hexToBin[strHex[i]]
    dec = strBinToDec(binary)
    return dec

def strDecToDec(strDec):
    # Convert string decimal to decimal
    return int(strDec)

def strArrayBinToDec(arrayBin, invert = False):
    # Convert an string array of binary numbers to a decimal number 
    forRange = range(0, len(arrayBin))
    if invert:
        forRange = range(len(arrayBin) - 1, 0, -1)
    strBin = ""
    for i in forRange:
        strBin = strBin + arrayBin[i - 1] 
    return strBinToDec(strBin)