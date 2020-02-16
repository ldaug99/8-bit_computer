
RETRIES = 10





com = openCom("COM4",115200)
time.sleep(0.1)
reply = com.readline()

address = 4909

com.write(address)
#com.write(b'data')
time.sleep(0.1)
reply = com.readline()
print(reply)
com.close()