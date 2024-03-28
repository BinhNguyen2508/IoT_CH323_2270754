print("Sensors and Actuators")

import time
import serial.tools.list_ports
# from pyngrok import ngrok

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
    # return "/dev/ttyUSB1"

# portName = "/dev/ttyUSB1"
# print(portName)
port = getPort()
try:
    ser = serial.Serial(port, baudrate=115200)
    print("Open " + port + " successfully")
except:
    print("Can not open port " + port)

relay3_ON  = [4, 6, 0, 0, 0, 255, 223, 201] #201, 223
relay3_OFF = [4, 6, 0, 0, 0, 0, 159, 137]#137, 159
# soil_temperature =[1, 3, 0, 6, 0, 1, 100, 11]
# soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]

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

def setRelay3(state):
    if state == True:
        ser.write(relay3_ON)
    else:
        ser.write(relay3_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

# def readTemperature():
#     serial_read_data(ser)
#     ser.write(soil_temperature)
#     time.sleep(1)
#     return serial_read_data(ser)

# def readMoisture():
#     serial_read_data(ser)
#     ser.write(soil_moisture)
#     time.sleep(1)
#     return serial_read_data(ser)

while True:
    print("TEST RELAY")
    setRelay3(True)
    time.sleep(2)
    setRelay3(False)
    time.sleep(2)

# while True:
#     print("TEST SENSOR")
#     print(readMoisture())
#     time.sleep(1)
#     print(readTemperature())
#     time.sleep(1)