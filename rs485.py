# print("Sensors and Actuators")

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

relay2_ON  = [3, 6, 0, 0, 0, 255, 201, 138] #201, 223
relay2_OFF = [3, 6, 0, 0, 0, 0, 202, 137]#137, 159

relay3_ON  = [4, 6, 0, 0, 0, 255, 200, 91] #201, 223
relay3_OFF = [4, 6, 0, 0, 0, 0, 136, 27]#137, 159

soil_temperature =[3, 3, 0, 6, 0, 1, 100, 11]
soil_moisture = [3, 3, 0, 7, 0, 1, 53, 203]

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

def setRelay2(ser, state):
    print('Set relay 2 to ' + str(state))
    if state == True:
        ser.write(relay2_ON)
    else:
        ser.write(relay2_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

def setRelay3(ser, state):
    print('Set relay 3 to ' + str(state))
    if state == True:
        ser.write(relay3_ON)
    else:
        ser.write(relay3_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

def readTemperature(ser):
    print('Reading temperature sensor..')
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser)

def readMoisture(ser):
    print('Reading humidity sensor..')
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)