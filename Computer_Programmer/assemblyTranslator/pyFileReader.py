# Simple functions for reading lines from a file

def readLinesInFiles(fileName, directory = ""):
    # Read lines in file
    # Input:
    # fileName: Name of file to read (with file extension), example: "myFile.txt"
    # directory (optional): Directory to search (relative or global) (should not include tailing "/"), example: "Documents/Python"
    path = fileName
    if directory != "": # Check if directory is given
        path = directory + "\\" + fileName # Add directory to path
    lines = [] # Buffer for lines
    try:
        with open(path, 'r') as file: # Open file
            doRun = True 
            while doRun:
                line = file.readline() # Read line
                if line != "": # Check if line not empty. Newlines in file will contain '\n' character
                    lines.append(line)
                else: # Line will be empty when there are no more lines in file.
                    doRun = False
        return lines
    except:
        print("Exception on readLinesInFiles(): No file with name {} found.".format(fileName))
        return None

def getCharPos(line, character):
    # Get position(s) of character in string
    charPos = []
    for i in range(0, len(line)):
        if line[i] == character:
            charPos.append[i]
    return charPos

def getStringPos(line, string):
    return line.find(string)

def excludeCharFromLines(lines, character, popEmpty = True):
    # Exclude a character from read lines
    # Input:
    # lines: Lines read from with function readLinesInFiles()
    # character: Character to remove from lines
    index = 0
    while index < len(lines):
        lines[index] = lines[index].replace(character, '')
        if popEmpty and lines[index] == '': # Check if lines is empty
            lines.pop(index)
        else:
            index = index + 1
    return lines

def excludePartAfterChar(lines, character, popEmpty = True):
    # Exclude rest of line from char
    index = 0
    while index < len(lines):
        charPos = lines[index].find(character)
        if charPos >= 0:
            lines[index] = lines[index][0:charPos]
            if popEmpty and lines[index] == '': # Check if lines is empty
                lines.pop(index)
            else:
                index = index + 1
        else:
            index = index + 1
    return lines

def findStringInLines(lines, string):
    # Find a string in lines, return index of each line in which string is found
    foundLines = []
    for i in range(0, len(lines)):
        pos = lines[i].find(string)
        if pos >= 0:
            foundLines.append(i)
    return foundLines
