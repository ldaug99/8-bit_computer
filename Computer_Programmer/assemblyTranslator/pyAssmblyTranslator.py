# Assembly to program line string translator intended for use with the Arduino project computerProgrammer
# This script expects a .asm file with :
# - A .data section containing constant variable data
# - A .bss section containing mofifiable variable data
# - A .text section with the program instructions

# Imports
import pyFileReader
import pyNumberSystems

# Sections
dataSection = "data"
bssSection = "bss"
textSection = "text"
sections = ["section .data", "section .bss", "section .text"]

# Memory location
typeInst = "inst"
typeLabl = "labl"
decInst = 105
decData = 100

# Local instruction and data memory
dataAddrCnt = 0
instAddrCnt = 0
dataMem = {}
instMem = {}

# Data types
dataTypes = ["db"]
maxPartsPerLine = 6

# Instruction set architecture file name
isaFileName = "instructionSet.txt"
isaDirectory = ""

def findSections(lines):
    # Find line num of sections, returns array with index of sections
    # Output: [data section, bss section, text section]
    sectionsPos = [-1, -1, -1] # Sections position 
    for i in range(0, len(sections)):
        sectionLineNum = pyFileReader.findStringInLines(lines, sections[i])
        secLength = len(sectionLineNum)
        if secLength == 0:
            print("Exception on findSections(): Section \"{}\" not found.".format(sections[i]))
        elif secLength > 1:
            print("Exception on findSections(): Duplicated section \"{}\n.".format(sections[i]))
        else:
            sectionsPos[i] = sectionLineNum[0]
    return sectionsPos

def getSectionsLength(sectionsPos, numLines):
    # Gets length of each section
    # Output: [data section, bss section, text section]
    # Sort array and find length between each sorted element (or length between last element and number of lines)
    sortedArray = sortArray(sectionsPos)
    sortedArrayLen = []
    for i in range(0, len(sortedArray)):
        if i >= len(sortedArray) - 1:
            sortedArrayLen.append((numLines - sortedArray[i]))
        else:
            sortedArrayLen.append((sortedArray[i + 1] - sortedArray[i]))
    # Translated to array with [section data, section bss, section text]
    sectionsPosLength = []
    for i in range(0, len(sectionsPos)):
        for k in range(0, len(sortedArray)):
            if sectionsPos[i] == sortedArray[k]:
                sectionsPosLength.append(sortedArrayLen[k])
    return sectionsPosLength

def sortArray(inArray):
    # Sort array of numbers
    newArray = inArray[:]
    sort = True
    index = 0
    while(sort):
        thisData = newArray[index]
        nextData = newArray[index + 1]
        if nextData < thisData:
            newArray[index] = nextData
            newArray[index + 1] = thisData
            if index > 0:
                index = index - 1 # Decrement to last index
        else:
            index = index + 1
        if index >= len(newArray) - 1:
            sort = False
    return newArray
    
def readVaraibleSection(lines, secPos, secLength):
    # Read each line in data or bss section
    secPos = secPos + 1 # Exclude section position
    secLength = secLength - 1 # Exclude section position
    translatedLines = []
    for i in range(secPos, secPos + secLength): # For each line in section
        stringParts = splitToParts(lines[i])
        translatedLine = processParts(stringParts)
        translatedLines.append(translatedLine)
    return translatedLines

def splitToParts(string):
    # Split a comma seperated string into an array of parts
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

def processParts(stringParts):
    # Convert string parts to array [memory location, addr, data0, data1, data2, data3]
    global dataAddrCnt
    global dataMem
    variableName = stringParts[0]
    variableType = stringParts[1]
    if variableType not in dataTypes:
        print("Exception on processVariable(): Invalid data type.")
        return None
    variableData = []
    for i in range(2, len(stringParts)):
        dec = convertToDec(stringParts[i])
        variableData.append(dec)
    for i in range(len(stringParts), maxPartsPerLine):
        variableData.append(0)
    dataMem[variableName] = dataAddrCnt # Save address to variable
    translatedLine = [decData, dataAddrCnt]
    for i in range(0, len(variableData)):
        translatedLine.append(variableData[i])
    dataAddrCnt = dataAddrCnt + 1
    return translatedLine

def convertToDec(valueString):
    valueType = valueString[len(valueString) - 1]
    valueString = valueString[0:len(valueString) - 1]
    if valueType == "h": # Is hex
        return pyNumberSystems.strHexToDec("0x" + valueString)
    elif valueType == "b": # Is binary
        return pyNumberSystems.strBinToDec(valueString)
    elif valueType == "d": # Is decimal
        return pyNumberSystems.strDecToDec(valueString)
    else:
        print("Exception on convertValue() -> Invalud value type.")
        return None

def readTextSection(lines, secPos, secLength):
    # What am I doing here?? O.o
    global instAddrCnt
    global instMem
    rawisa = pyFileReader.readLinesInFiles(isaFileName, isaDirectory)
    isa = processISA(rawisa)
    secPos = secPos + 1 # Exclude section position
    secLength = secLength - 1 # Exclude section position


    data = lines
    pos = secPos
    lenght = secLength

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

    translatedLines = []
    for i in range(0, len(instructions)):
        address = instructions[i][0]
        opcode = isa[instructions[i][1][1]]
        data0 = getInstData(instructions, i, 0)
        data1 = getInstData(instructions, i, 1)
        data2 = getInstData(instructions, i, 2)
        translatedLine = [
            decInst, address, opcode, data0, data1, data2
        ]
        translatedLines.append(translatedLine)
    return translatedLines

def processISA(rawisa):
    isa = {}
    for i in range(0, len(rawisa)):
        string = rawisa[i]
        commaPos = string.find(",")
        opcode = string[0:commaPos]
        string = string[commaPos + 1::]
        commaPos = string.find(",")
        binary = string[0:commaPos]
        isa[opcode] = pyNumberSystems.strBinToDec(binary)
    return isa

def getInstData(instructions, index, length):
    data = 0
    if len(instructions[index][1][2]) > length:
        variable = instructions[index][1][2][0]
        if variable in dataMem:
            data = dataMem[instructions[index][1][2][length]]
        elif variable in instMem:
            data = instMem[instructions[index][1][2][length]]
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

def appendTranslatedLines(programLines, translatedLines):
    allLines = programLines[:]
    for i in range(0, len(translatedLines)):
        allLines.append(translatedLines[i])
    return allLines

def printArray(arrayToPrint):
    for i in range(0, len(arrayToPrint)):
        print(arrayToPrint[i])

def translateFromAssembly(fileName, directory = ""):
    # Read program lines from file
    programLines = pyFileReader.readLinesInFiles(fileName, directory)
    # Remove comment and newlines
    programLines = pyFileReader.excludePartAfterChar(programLines, ';')
    programLines = pyFileReader.excludePartAfterChar(programLines, '\n')
    # Get length of program
    programLength = len(programLines)
    # Find sections
    sectionPos = findSections(programLines)
    # Find section length
    sectionLength = getSectionsLength(sectionPos, programLength)
    # Prepare program array and data memory
    translatedProgram = []
    # Read data section and bss section
    for i in range(0, 2):
        translatedLines = readVaraibleSection(programLines, sectionPos[i], sectionLength[i])
        # Append translated lines
        translatedProgram = appendTranslatedLines(translatedProgram, translatedLines)
    # Read text section
    translatedLines = readTextSection(programLines, sectionPos[2], sectionLength[2])
    # Append translated lines
    translatedProgram = appendTranslatedLines(translatedProgram, translatedLines)
    # Print translated program
    # rintArray(translatedProgram)
    # Return translated program
    return translatedProgram

def partsToString(lineParts):
    string = ""
    length = len(lineParts)
    for i in range(0, length):
        if (i == length - 1):
            string = string + str(lineParts[i])
        else:
            string = string + str(lineParts[i]) + ", "
    return string

def writeProgramToHfile(translatedProgram):
    # Write translated lines to Arduino H file.
    # Get number of lines
    linesToProgram = len(translatedProgram)
    # Setup file line buffer
    lineBuffer = [
        "#include <Arduino.h> \n",
        "const static uint8_t programLength = " + str(linesToProgram) + "; \n",
        "const static uint8_t lineParts = 6; \n"
        "const static uint8_t programData[programLength][lineParts] = { \n",
    ]
    endLine = "}; \n"
    # Add program lines
    for i in range(0, linesToProgram):
        lineParts = translatedProgram[i]
        if (i == linesToProgram - 1):
            line = "    {" + partsToString(lineParts) + "} \n"
        else:
            line = "    {" + partsToString(lineParts) + "},\n"
        lineBuffer.append(line)
    lineBuffer.append(endLine)
    with open("program.h", 'w') as file:
        for i in range(0, len(lineBuffer)):
            file.write(lineBuffer[i])

fileName = "AddSubLoop.asm", 
directory = "8-bit_computer_programs"

translatedProgram = translateFromAssembly("simpleAddLoop.asm", "8-bit_computer_programs")
writeProgramToHfile(translatedProgram)