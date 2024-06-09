import time
import serial.tools.list_ports
from constants import*
import random
class serialCommunication:
    def __init__(self):

        self.portName = self.getPort()
        try:
            self.ser = serial.Serial(port=self.portName, baudrate=9600)
            print("Open successfully")
        except:
            print("Can not open the port")
    
    def getPort(self):
        ports = serial.tools.list_ports.comports()
        N = len(ports)
        commPort = "None"
        for i in range(0, N):
            port = ports[i]
            strPort = str(port)
            if "USB" in strPort:
                splitPort = strPort.split(" ")
                commPort = (splitPort[0])
        return commPort
        # return "/dev/ttyUSB1"

    def readData(self):
        bytesToRead = self.ser.inWaiting()
        if bytesToRead > 0:
            out = self.ser.read(bytesToRead)
            data_array = [b for b in out]
            print("Array:", data_array)
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                return value
            else:
                return -1
        return 0

    def setDevice(self, id, state):
        if state == True:
            print("Turn ON Relay ", id, ": ", relay_ON[id], "--------")
            self.ser.write(relay_ON[id])
        else:
            print("Turn OFF Relay ", id, ": ", relay_OFF[id], "--------")
            self.ser.write(relay_OFF[id])
        time.sleep(0.1)
        print("Result: ", self.readData())

    def readTemperature(self):
        # return random.randint(20,40)
        self.readData()
        self.ser.write(soil_temperature)
        time.sleep(0.1) 
        #change to task
        return self.readData()

    def readMoisture(self):
        # return random.randint(50,80)
        self.readData()
        self.ser.write(soil_moisture)
        time.sleep(0.1) 
        #change to task
        return self.readData()   
    
    def readAllSensors(self):
        return self.readTemperature(), self.readMoisture()
    

RS485 = serialCommunication() 
# for i in range(1,9):
#     UART.ser.setDevice(i, True)
#     time.sleep(1)
#     print(serial.ser.readAllSensors())
#     time.sleep(1)

# print("------------------")
# for i in range(1,9):
#     UART.ser.setDevice(i, False)
#     time.sleep(1)
#     print(serial.ser.readAllSensors())
