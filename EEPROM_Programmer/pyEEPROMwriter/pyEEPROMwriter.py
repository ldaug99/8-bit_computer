import serial
from serial.tools import list_ports
import time

class pyEEPROM():

    def __init__(self, port = None, baud = None):
        self.__port = port
        self.__baud = baud
        if self.__port != None and self.__baud != None:
            self.start(self.__port, self.__baud)

    def getPorts(self):
        print("Avaliable COM ports are:")
        list_ports.main()
        print("")

    def start(self, port, baud):
        if self.__port != None and self.__baud != None:
            self.__com = serial.Serial(port, baud, timeout = 1)
            time.sleep(0.5)
            self.__com.readline()
            print("COM port set to {} with baud {}. COM port is open: {}".format(port, baud, self.__com.is_open))
            print(" ")

    def close(self):
        print("Closing serial port...", end = '')
        self.__com.close()
        if not self.__com.is_open:
            print(" Success.")
        else:
            print(" Failed")
        print(" ")

    def write(self, address, data):
        failedToWrite = []
        print("Writing entry...")
        check = self.__writeAddress(self.__com, address[i], data[i])
        if check != None:
            failedToWrite.append(address)
        failedVerification = []
        print("Validating entry...")
        check = self.__validateAddress(self.__com, address[i], data[i])
        if check != None:
            failedVerification.append(address)
        return failedToWrite, failedVerification

    def writeArray(self, address, data):
        failedToWrite = []
        for i in range(0, len(address)):
            print("Writing entry {} of {} entries...".format(i + 1, len(address)))
            check = self.__writeAddress(self.__com, address[i], data[i])
            if check != None:
                failedToWrite.append(address[i])
        failedVerification = []
        # for i in range(0, len(address)):
        #     print("Validating entry {} of {} entries...".format(i + 1, len(address)))
        #     check = self.__validateAddress(self.__com, address[i], data[i])
        #     if check != None:
        #         failedVerification.append(address[i])
        return failedToWrite, failedVerification

    def __writeAddress(self, com, address, data):
        print("Writing to address {} with data {}... ".format(address, data), end = '')
        output = str(address) + "," + str(data)
        com.write(output.encode())
        time.sleep(0.01)
        reply = com.readline()
        if reply.decode() == "OK\r\n":
            print("OK")
            return None
        else:
            print("No reply from programmer... Failed")
            return address

    def __validateAddress(self, com, address, expdata):
        com.flush()
        print("Validating address {} with expected data {}... ".format(address, expdata), end = '')
        output = str(address)
        com.write(output.encode())
        time.sleep(0.1)
        reply = com.readline()
        reply = reply.decode()[:-2]
        point = reply.find(",")
        try:
            addr = int(reply[0:point])
            data = int(reply[point + 1::])
        except:
            print("Unexpected return, retrying...")
            return self.__validateAddress(self.__com, address, expdata)
        print("Found data {}... ".format(reply), end = '')
        if data == expdata:
            print("OK")
            return None
        else:
            print("Failed")
            return address