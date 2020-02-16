
numBits = 8

secToEEPROMio = {
    "A": 2,
    "B": 1,
    "C": 0,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "DP": 7
}

EEPROMioToSec = {
    0: "C",
    1: "B",
    2: "A",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "DP"
}

digitToSec = {
    "0": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "F": 1, "G": 0, "DP": 0},
    "1": {"A": 0, "B": 1, "C": 1, "D": 0, "E": 0, "F": 0, "G": 0, "DP": 0},
    "2": {"A": 1, "B": 1, "C": 0, "D": 1, "E": 1, "F": 0, "G": 1, "DP": 0},
    "3": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 0, "F": 0, "G": 1, "DP": 0},
    "4": {"A": 0, "B": 1, "C": 1, "D": 0, "E": 0, "F": 1, "G": 1, "DP": 0},
    "5": {"A": 1, "B": 0, "C": 1, "D": 1, "E": 0, "F": 1, "G": 1, "DP": 0},
    "6": {"A": 1, "B": 0, "C": 1, "D": 1, "E": 1, "F": 1, "G": 1, "DP": 0},
    "7": {"A": 1, "B": 1, "C": 1, "D": 0, "E": 0, "F": 0, "G": 0, "DP": 0},
    "8": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "F": 1, "G": 1, "DP": 0},
    "9": {"A": 1, "B": 1, "C": 1, "D": 1, "E": 0, "F": 1, "G": 1, "DP": 0},
    "-": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 1, "DP": 0},
    "N": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "DP": 0}
}

adcList = ["A", "B", "C", "D", "E", "F", "G", "DP"]

# EEPROM uses A8 and A9 as digit place select.
# Digit place 0 is first digit, 1 is second digit and so on.
# "132", 2 is digit place 0, 3 is digit place 1 and 1 is digit place 2.
digitPlaceToEEPROM = {
    0: [0, 0],
    1: [1, 0],
    2: [0, 1],
    3: [1, 1]
}
# First digit select addres is on A8. 8'bit is lower select address.
lowSelectAddrLocation = 8

maxDigits = 4

def processEachDidget():
    eepromDigits = [[], []]
    for i in range(0, (2**numBits - 1)):
        strDec = str(i)
        for k in range(len(strDec), maxDigits):
            strDec = "N" + strDec
        for k in range(0, len(strDec)):
            eepromAddr = i
            eepromSelect = digitPlaceToEEPROM[k]
            for h in range(0, len(eepromSelect)):
                eepromAddr = eepromAddr + eepromSelect[h] * (2**(lowSelectAddrLocation + h))
            eepromData = 0
            preIOconvert = digitToSec[strDec[(len(strDec) - 1) - k]]
            if len(preIOconvert) != len(EEPROMioToSec):
                print("What, no")
                while(1==1):
                    pass
            for h in range(0, len(EEPROMioToSec)):
                eepromData = eepromData + preIOconvert[EEPROMioToSec[h]] * (2**h)
                #print("EEPROMioToSec[h] is: {}, preIOconvert[EEPROMioToSec[h]] is {}, data is: {}".format(EEPROMioToSec[h], preIOconvert[EEPROMioToSec[h]], eepromData))
            #print("Decimal {}, part {}, has address {} and data {}, ".format(strDec, strDec[(len(strDec) - 1) - k], eepromAddr, eepromData))
            eepromDigits[0].append(eepromAddr)
            eepromDigits[1].append(eepromData)
        #print("Done")
    #for i in range(0, len(eepromDigits)):
    #    print(eepromDigits[i])
    #print("Total entrys {}".format(len(eepromDigits)))
    return eepromDigits