import json

def loadCSV(fileName, directory = ""):
    print("Loading file {}...".format(fileName), end = '')
    csvData = __getDataFromCSV(fileName, directory)
    data, fetch = __sepFetchFromData(csvData)
    newData = __addFetchCycleToOperation(data, fetch)
    newData = __replaceFlagBits(newData)
    if newData != None:
        print("Ok.")
    else:
        print("Failed.")
    return newData

def splitToEEPROM(EEPROMnum, allData, addrPinCnt = 13, dataPinCnt = 8, EEPROMcnt = 4):
    address = []
    data = []
    for i in range(0, len(allData)):
        address.append(allData[i][0:addrPinCnt])
        data.append(allData[i][(addrPinCnt + dataPinCnt * (EEPROMnum - 1)):(addrPinCnt + (dataPinCnt * EEPROMnum))])
    return address, data

def __getDataFromCSV(file, directory = ""):
    fileDir = file
    if directory != "":
        fileDir = directory + "\\" + file
    lines = []
    with open(fileDir, "r") as file: 
        lis = [line.split() for line in file]
        for line in lis:
            lines.append(line[0].split(","))
    return lines

def __sepFetchFromData(rawData):
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

def __addFetchCycleToOperation(data, fetch):
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

def __replaceFlagBits(data):
    newData = data[:]
    i = 0
    while (i < len(newData)):
        popItem = False
        for k in range(0, len(newData[i])):
            if newData[i][k] == "x" and not popItem:
                popItem = True
                for h in range(0,2):
                    temp = newData[i][:]
                    temp[k] = str(h)
                    newData.append(temp)
        if popItem:
            newData.pop(i)
            i = i - 1
        i = i + 1
    return newData