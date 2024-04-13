import time
import serial.tools.list_ports

import random

relay1_ON  = [4, 6, 0, 0, 0, 255, 200, 91] #Light
relay1_OFF = [4, 6, 0, 0, 0, 0, 136, 27] #Light
relay2_ON  = [5, 6, 0, 0, 0, 255, 201, 138] #Pump
relay2_OFF = [5, 6, 0, 0, 0, 0, 202, 137] #Pump

soil_temperature =[1, 3, 0, 6, 0, 1, 100, 11]
soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
soil_light = [1,1,1,1,1,1,1,1] #Placeholder address

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    print(commPort)
    return commPort

def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

def setRelay1_demo(state):
    print("Light Button is set to " + str(state))
    return state

def setRelay2_demo(state):
    print("Pump Button is set to " + str(state))
    return state

def readTemperature_demo(temp, pumpState):
    temp = temp + random.randrange(1, 2, 1) - pumpState*random.randrange(3, 4, 1)
    return temp

def readHumidity_demo(humid, pumpState):
    humid = humid - random.randrange(1, 3, 1) + pumpState*(random.randrange(4, 6, 1))
    return humid

def readLight_demo(light, lightState):
    light = 20 + lightState*150
    return light