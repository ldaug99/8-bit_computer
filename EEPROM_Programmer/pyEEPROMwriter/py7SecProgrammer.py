from pyEEPROMwriter import pyEEPROM
import py7secLogicGenerator

data = py7secLogicGenerator.processEachDidget()

promWriter = pyEEPROM("COM4", 115200)
failedWrite, failedVerify = promWriter.writeArray(data[0], data[1])

print("Failed to write: {}".format(failedWrite))
print("Failed to verify: {}".format(failedVerify))

promWriter.close()