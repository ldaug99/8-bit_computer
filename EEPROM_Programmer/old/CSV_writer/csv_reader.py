import json
import serial
from serial.tools import list_ports
import time



PORT = "COM4"
BAUD = 115200

LSBRIGHT = 0
MSBRIGHT = 1

com = None



def getDataFromCSV(file, directory = ""):
    fileDir = file
    if directory != "":
        fileDir = directory + "\\" + file
    lines = []
    with open(fileDir, "r") as file: 
        lis = [line.split() for line in file]
        for line in lis:
            lines.append(line[0].split(","))
    return lines

def sepFetchFromData(rawData):
    fetch = []
    poped = 0
    data = rawData[:]
    for i in range(0, len(rawData)):
        isFetch = True
        for k in range(0, 8):
            if rawData[i][k] != "x":
                isFetch = False
                break
        if isFetch:
            fetch.append(rawData[i])
    for i in range(0, len(fetch)):
        data.remove(fetch[i])
    return data, fetch

def addFetchCycleToOperation(data, fetch):
    data.append([0,0,0,0,0,0,0,0])
    newData = []
    opSteps = []
    opcode = [None, None, None, None, None, None, None, None]
    nextopcode = [None, None, None, None, None, None, None, None]
    opstart = 0
    i = 0
    while (i < len(data)):
        isSameOP = True
        for k in range(0, 8):
            if opcode[k] == None:
                opcode[k] = data[i][k]
            elif opcode[k] != data[i][k]:
                nextopcode = data[i][k]
                isSameOP = False
        if not isSameOP:
            for k in range(0, len(fetch)):
                newData.append(opcode[0:8] + fetch[k][8::])
            for k in range(opstart, i):
                newData.append(data[k][:]) 
            opcode = [None, None, None, None, None, None, None, None]
            opstart = i
            i = i - 1
            isSameOP = True
        i = i + 1
    return newData

def replaceFlagBits(data):
    newData = []
    for i in range(0, len(data)):
        if data[i][11] == "x" and data[i][12] == "x":
            newData.append(data[i][0:11] + ["0","0"] + data[i][13::])
            newData.append(data[i][0:11] + ["0","1"] + data[i][13::])
            newData.append(data[i][0:11] + ["1","0"] + data[i][13::])
            newData.append(data[i][0:11] + ["1","1"] + data[i][13::])
        elif data[i][11] == "x":
            newData.append(data[i][0:11] + ["0"] + data[i][12::])
            newData.append(data[i][0:11] + ["1"] + data[i][12::])
        elif data[i][12] == "x":
            newData.append(data[i][0:12] + ["0"] + data[i][13::])
            newData.append(data[i][0:12] + ["1"] + data[i][13::])
    return newData






csvData = getDataFromCSV("logic.txt")
data, fetch = sepFetchFromData(csvData)
newData = addFetchCycleToOperation(data, fetch)
newData = replaceFlagBits(newData)

for i in range(0, len(newData)):
    print(newData[i])

#eeprom0data = splitToEEPROM(0, csvData)
#eeprom1data = splitToEEPROM(1, csvData)
#eeprom2data = splitToEEPROM(2, csvData)
#eeprom3data = splitToEEPROM(3, csvData)


def splitToEEPROM(EEPROMnum, data, addrPinCnt = 13, dataPinCnt = 8, EEPROMcnt = 4):
    pass



def readCSV(numAddressPin = 13, numDataPin = 8, EEPROMnum = 4):
    EEPROM = {}
    for num in range(0, EEPROMnum):
        temp = {}
        for line in range(0, len(lineList)):
            address = lineList[line][0:numAddressPin]
            data = lineList[line][numAddressPin+(numDataPin*num):numAddressPin+(numDataPin*(num+1))]
            temp[line] = {"address": address, "data": data}
        EEPROM[num] = temp
    return EEPROM

def wrtieEEPROM(eepromNr):
    dictionary = readCSV()
    print("Programming EEPROM nr {}".format(eepromNr))
    addressToWrite = []
    dataToWrite = []
    for instNum in dictionary[eepromNr - 1]:
        inst = dictionary[eepromNr - 1][instNum]
        address = inst["address"]
        data = inst["data"]
        eAddress = binStringToInts(address)
        eData = binStringToInts(data)
        for i in range(0, len(eAddress)):
            addressToWrite.append(eAddress[i])
            dataToWrite.append(eData)
    print("Writing {} entries to EEPROM...")
    totalAddresses = len(addressToWrite)
    for i in range(0, totalAddresses):
        print("Writing address {} with data {}".format(addressToWrite[i], dataToWrite[i]))
        writeToAddress(addressToWrite[i], dataToWrite[i])
        print("Wrote entry {} of {} entries".format(i,totalAddresses - 1))
    for i in range(0, totalAddresses):
        checkData(addressToWrite[i], dataToWrite[i])

def getPorts():
    list_ports.main()

def openCom(port = PORT, baud = BAUD):
    com = serial.Serial(port, baud, timeout = 1)
    attempts = 0
    while not com.is_open:
        attempts = attempts + 1
        com.open()
        if attempts > RETRIES:
            print("Exception on openCOM(): Unable to start serial communication on port {}".format(port))
            return None
    time.sleep(1)
    com.readline()
    return com

def checkData(address, data):
    output = str(address)
    com.write(output.encode())
    time.sleep(0.1)
    reply = com.readline()
    if int(reply.decode()) != data:
        print("ERROR on address {}, with data {}. Expected data {}.".format(address, reply.decode(), data))

def writeToAddress(address, data):
    output = str(address) + "," + str(data)
    writeToCom(output)
    
def writeToCom(message):
    com.write(message.encode())
    time.sleep(0.1)
    #reply = com.read(4)
    #print(reply)
    #if reply == b"OK\r\n":
    #    pass
    #else:
    #    print("EEPROM did not responde to command")

def closeCom():
    com.close()

def binStringToInts(binString, bitOrder = MSBRIGHT):
    numBits = len(binString)
    baseInt = 0
    index = 0
    wildBitsPow = []
    for bit in binString:
        if bit == "x":
            wildBitsPow.append(index)
        elif int(bit) == 1: 
            baseInt = baseInt + bitToInt(index, MSBRIGHT, numBits)
        index = index + 1
    if len(wildBitsPow) != 0:
        numWildInts = 2 ** len(wildBitsPow)
        numBinWild = len(bin(numWildInts - 1)[2::])
        ints = []
        for i in range(0, numWildInts):
            wildInt = baseInt
            bits = bin(i)[2::]
            diff = numBinWild - len(bits)
            if diff > 0:
                zeros = ""
                for i in range(0, diff):
                    zeros = zeros + "0"
                bits = zeros + bits
            for k in range(0, numBinWild):
                bit = int(bits[k])
                wildInt = wildInt + (bit * (2 ** wildBitsPow[k]))
            ints.append(wildInt)
        return ints
    else:
        return baseInt

def bitToInt(bitNum, bitOrder, numBits):
    bitInt = 0
    if bitOrder:
        bitInt = (2 ** bitNum)
    else:
        bitInt = (2 ** (bitNum - numBits))
    return bitInt

#com = openCom("COM4",115200)
#noice = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '0', '0', '0', 'x', 'x']
#noice = ["x", "x", "x", 0]
#print(binStringToInts(noice))
#wrtieEEPROM(1)
#readCSV()
#closeCom()