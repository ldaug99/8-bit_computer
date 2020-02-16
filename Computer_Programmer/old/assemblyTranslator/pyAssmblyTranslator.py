# Assembly to program line string translator intended for use with the Arduino project computerProgrammer
# This script expects a .asm file with :
# - A .data section containing constant variable data
# - A .bss section containing mofifiable variable data
# - A .text section with the program instructions

import serial
import time

dataSection = "data"
bssSection = "bss"
textSection = "text"

typeInst = "inst"
typeLabl = "labl"

dataTypes = ["db"]

dataAddrCnt = 0
dataMem = {}
instMem = {}

translatedProgram = []

binToHex = {
    "0000": "0",
    "0001": "1",
    "0010": "2",
    "0011": "3",
    "0100": "4",
    "0101": "5",
    "0110": "6",
    "0111": "7",
    "1000": "8",
    "1001": "9",
    "1010": "A",
    "1011": "B",
    "1100": "C",
    "1101": "D",
    "1110": "E",
    "1111": "F"
}

decToHex = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "A",
    11: "B",
    12: "C",
    13: "D",
    14: "E",
    15: "F"
}


def readFile(fileName, directory = ""):
    path = fileName
    if directory != "":
        path = directory + "\\" + fileName
    lines = []
    with open(path, 'r') as file:
        doRun = True
        while doRun:
            try:
                line = file.readline()
                if line != "":
                    lines.append(line)
                else:
                    doRun = False
            except:
                print("Execption on readASMfile() -> Failed to read line from ASM file. Translation failed.")
    return lines, len(lines)

def removeComment(data):
    return excludeCharacter(data, ';')

def removeNewLine(data):
    return excludeCharacter(data, '\n')

def getStringPos(line, string):
    return line.find(string)

def excludeCharacter(data, char):
    lines = []
    for i in range(0, len(data)):
        charPos = getStringPos(data[i], char)
        if charPos < 0: # -1 if not found
            #print(data[i])
            lines.append(data[i])
        if charPos > 0: # 0 if at first position. Exclude 0
            #print(data[i][0:charPos])
            lines.append(data[i][0:charPos])
    return lines

def findSections(data):
    posArr = [None, None, None]
    tempPos = [-1,-1,-1]
    for i in range(0, len(data)):
        tempPos[0] = getStringPos(data[i], "section .data")
        tempPos[1] = getStringPos(data[i], "section .bss")
        tempPos[2] = getStringPos(data[i], "section .text")
        for k in range(0, len(tempPos)):
            if tempPos[k] >= 0:
                if posArr[k] == None:
                    posArr[k] = i
                else:
                    print("Exception on findSections() -> Duplicated section. Translation failed.")
    return posArr

def validateSections(posArr):
    valid = True
    for i in range(0, len(posArr) - 1):
        if posArr[i] == None or posArr[i + 1] == None or posArr[i] > posArr[i + 1]:
            valid = False
    return valid

def readDataSection(data, pos, lenght):
    readSection(dataSection, data, pos, lenght)

def readBssSection(data, pos, lenght):
    readSection(bssSection, data, pos, lenght)

def readSection(section, data, pos, lenght):
    pos = pos + 1 # Exclude section position
    lenght = lenght - 1 # Exclude section position
    for i in range(pos, pos + lenght):
        stringParts = splitToParts(data[i])
        translatedLine = processParts(section, stringParts)
        translatedProgram.append(translatedLine)

def splitToParts(string):
    notSpaceIndex = []
    for i in range(0, len(string)):
        if string[i] != " ":
            notSpaceIndex.append(i)
    stringParts = []
    processing = True
    index = 0
    maxIndex = len(notSpaceIndex)
    part = ""
    while(processing):
        part = part + string[notSpaceIndex[index]]
        if index == maxIndex - 1:
            stringParts.append(part)
            processing = False
        elif index < maxIndex and notSpaceIndex[index] != notSpaceIndex[index + 1] - 1:
            stringParts.append(part)
            part = ""
        index = index + 1
    return stringParts

def processParts(section, stringParts, flag = False):
    global dataAddrCnt
    if section == dataSection or section == bssSection:
        variableName, variableValue = processVariable(stringParts)
        dataMem[variableName] = dataAddrCnt # Save address to variable
        translatedLine = "d, " + "0x" + str(decimalToHex(dataAddrCnt)) + ", " + variableValue + ", 0x00, "  + "0x00, "  + "0x00"
        dataAddrCnt = dataAddrCnt + 1
        return translatedLine
    else:
        print("Exception on processParts() -> Invalid section.")
        return None

def processVariable(stringParts):
    variableName = stringParts[0]
    variableType = stringParts[1]
    variableValue = stringParts[2]
    if variableType not in dataTypes:
        print("Exception on processVariable() -> Invalid data type.")
    hexString = convertValue(variableValue)
    return variableName, hexString

def convertValue(valueString):
    valueType = valueString[len(valueString) - 1]
    valueString = valueString[0:len(valueString) - 1]
    if valueType == "h": # Is hex
        return "0x" + valueString[0 : len(valueString)]
    elif valueType == "b": # Is binary
        return "0x" + binaryToHex(valueString)
    elif valueType == "d": # Is decimal
        return "0x" + strDecimalToHex(valueString)
    else:
        print("Exception on convertValue() -> Invalud value type.")
        return None

def strDecimalToHex(valueString):
    if int(valueString) > 255:
        print("Exception on decimalToHex() -> Only unsigned 8-bit values are allowed")
    quotient = int(int(valueString) / 16)
    reminder = int(int(valueString) % 16)
    #print("Deciaml is {}, hex is: {}".format(valueString, decToHex[quotient] + decToHex[reminder]))
    return decToHex[quotient] + decToHex[reminder]

def decimalToHex(decimal):
    quotient = int(decimal / 16)
    reminder = int(decimal % 16)
    #print("Deciaml is {}, hex is: {}".format(decimal, decToHex[quotient] + decToHex[reminder]))
    return decToHex[quotient] + decToHex[reminder]

def strBinToDec(strBin):
    # Convert a binary number (as string) to a deicmal number
    # MSB is left most bit
    # Input example: "1101001", Output: 105
    # Output
    dec = 0
    for i in range(len(strBin),0,-1):
        dec = dec + int(strBin[len(strBin) - i]) * (2 ** (i - 1))
    return dec

def binaryToHex(valueString):
    try:
        hexParts = [
            valueString[0:4],
            valueString[4:len(valueString)]
        ]
        hexString = ""
        for i in range(0, len(hexParts)):
            hexString = hexString + binToHex[hexParts[i]]
        return hexString
    except:
        print("Exception on binaryToHex() -> Invalid binary number.")

def processISA(rawisa):
    isa = {}
    for i in range(0, len(rawisa)):
        string = rawisa[i]
        commaPos = string.find(",")
        opcode = string[0:commaPos]
        string = string[commaPos + 1::]
        commaPos = string.find(",")
        binary = string[0:commaPos]
        isa[opcode] = binaryToHex(binary)
    return isa

def readTextSection(data, pos, lenght):
    rawisa, isaLenght = readFile("instructionSet.txt")
    isa = processISA(rawisa)
    pos = pos + 1 # Exclude section position
    lenght = lenght - 1 # Exclude section position
    textLines = []
    for i in range(pos, pos + lenght):
        stringParts = splitToParts(data[i])
        textLines.append(processInstruction(stringParts))
    instructions = []
    labels = []
    instCnt = 0
    for i in range(0, len(textLines)):
        if textLines[i][0] == typeLabl:
            labels.append([instCnt,textLines[i][2][0]])
        else:
            instructions.append([instCnt, textLines[i]])
            instCnt = instCnt + 1
    for i in range(0, len(labels)):
        instMem[labels[i][1]] = labels[i][0]
    print(instMem)
    print(instructions)
    for i in range(0, len(instructions)):
        address = str(decimalToHex(instructions[i][0]))
        opcode = isa[instructions[i][1][1]]
        data1 = getInstData(instructions, i, 0)
        data2 = getInstData(instructions, i, 1)
        data3 = getInstData(instructions, i, 2)
        translatedLine = "i, " + "0x" + address + ", 0x" + opcode + ", 0x" + data1 + ", 0x" + data2 + ", 0x" + data3
        translatedProgram.append(translatedLine)

def getInstData(instructions, index, length):
    data = "00"
    if len(instructions[index][1][2]) > length:
        variable = instructions[index][1][2][0]
        if variable in dataMem:
            data = decimalToHex(dataMem[instructions[index][1][2][length]])
        elif variable in instMem:
            data = decimalToHex(instMem[instructions[index][1][2][length]])
    return data

def processInstruction(stringParts):
    instruction = stringParts[0]
    variables = []
    textType = typeInst
    for i in range(0, len(stringParts) - 1):
        variables.append(stringParts[i + 1])
    colorPos = instruction.find(":")
    if colorPos >= 0:
        textType = typeLabl
        instruction = None
        variables.append(stringParts[0][0:len(stringParts) - 2])
    return [textType, instruction, variables]

def translate(file, directory):
    progLines, lenght = readFile(file, directory)
    #progLines, lenght = readFile("simpleAddLoop.asm", "8-bit_computer_programs")
    #progLines, lenght = readFile("AddSubLoop.asm", "8-bit_computer_programs")
    progLines = removeComment(progLines)
    progLines = removeNewLine(progLines)
    posArr = findSections(progLines)
    valid = validateSections(posArr)
    if valid:
        readDataSection(progLines, posArr[0], (posArr[1] - posArr[0]))
        readBssSection(progLines, posArr[1], (posArr[2] - posArr[1]))
        readTextSection(progLines, posArr[2], (len(progLines) - posArr[2]))
    else:
        print("Expection on .... -> Invalid section declaration: Missing or missplaced sections.")
    with open("program.txt", 'w') as file:
        for i in range(0, len(translatedProgram)):
            file.write(translatedProgram[i] + "\n")

def upload(uploadArr, port, baud):
    com = serial.Serial(port, baud, timeout = 1)
    time.sleep(0.5)
    com.readline()
    print("COM port set to {} with baud {}. COM port is open: {}".format(port, baud, com.is_open))
    print("Uploading...")
    for i in range(0, len(uploadArr)):
        print("Uploading line {} of {} lines.".format(i + 1, len(uploadArr)))
        print("Lines is: {} ".format(uploadArr[i]), end = '')
        com.write(uploadArr[i].encode())
        time.sleep(0.1)
        waitForOK = True
        while(waitForOK):
            reply = com.readline()
            if reply.decode() == "OK\r\n":
                waitForOK = False

translate("AddSubLoop.asm", "8-bit_computer_programs")
#upload(translatedProgram, "COM4", 115200)



    # linesToProgram = len(translatedProgram)
    # defProgramLines = "const static uint8_t programLength = " + str(linesToProgram) + "; \n"
    # programLineArray = [
    #     "#include <Arduino.h> \n",
    #     defProgramLines,
    #     "const PROGMEM String programData[programLength] = { \n",
    # ]
    # # Add program lines
    # for i in range(0, len(translatedProgram)):
    #     programLine = translatedProgram[i]
    #     if (i == len(translatedProgram) - 1):
    #         programLineString = "   \"" + programLine + "\"\n"
    #     else:
    #         programLineString = "   \"" + programLine + "\",\n"
    #     programLineArray.append(programLineString)
    # endLine = "}; \n"
    # programLineArray.append(endLine)
    # with open("program.h", 'w') as file:
    #     for i in range(0, len(programLineArray)):
    #         file.write(programLineArray[i])



    #    programLineArray = [
    #     "#include <Arduino.h> \n",
    #     defProgramLines
    # ]
    # instTypeLine = "const PROGMEM String instType[programLength] = { \n   "
    # addrTypeLine = "const PROGMEM String addrType[programLength] = { \n   "
    # data0TypeLine = "const PROGMEM String data0Type[programLength] = { \n   "
    # data1TypeLine = "const PROGMEM String data1Type[programLength] = { \n   "
    # data2TypeLine = "const PROGMEM String data2Type[programLength] = { \n   "
    # data3TypeLine = "const PROGMEM String data3Type[programLength] = { \n   "
    # types = [instTypeLine, addrTypeLine, data0TypeLine, data1TypeLine, data2TypeLine, data3TypeLine]
    # endLine = "\n}; \n"

    # for i in range(0, len(types)):
    #     progLine = types[i]
    #     for k in range(0, len(translatedProgram)):
    #         lineData = translatedProgram[k][i]
    #         if (i == len(translatedProgram) - 1):
    #             progLine = progLine + "\"" + lineData + "\""
    #         else:
    #             progLine = progLine + "\"" + lineData + "\", "
    #     programLineArray.append(progLine)
    #     programLineArray.append(endLine)