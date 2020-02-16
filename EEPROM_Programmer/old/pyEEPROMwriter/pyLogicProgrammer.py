from pyEEPROMwriter import pyEEPROM
import pyCSVloader

data = pyCSVloader.loadCSV("logic.txt")

# From 1 to 4
eepromNr = 1
eepromData = pyCSVloader.splitToEEPROM(eepromNr, data)


promWriter = pyEEPROM("COM4", 115200)
failedWrite, failedVerify = promWriter.writeArray(eepromData[0], eepromData[1])

print("Failed to write: {}".format(failedWrite))
print("Failed to verify: {}".format(failedVerify))

promWriter.close()