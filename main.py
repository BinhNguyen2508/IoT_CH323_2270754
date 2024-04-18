import sys
import time
from os.path import exists
import cv2
from Adafruit_IO import MQTTClient
# from imageRegconition import *
from plant_disease_ai import *
from rs485 import *

DEFAULT_AUTOMATION_CONFIG = '15,45,50,200,20,80'

AIO_FEED_IDs = ["button1","button2","config"]
AIO_USERNAME = "nbinhsdh222"
AIO_KEY = ""

usb_port = ""
client = MQTTClient(AIO_USERNAME , AIO_KEY)

global tempLowerBound, tempUpperBound
global humidLowerBound, humidUpperBound
global lightLowerBound, lightUpperBound

#Set time_out to > 0 to prevent infinite loop
time_out = 300 #seconds
time_elapsed = 0 #seconds

#Loop interval step
interval_step = 1 #seconds

sensor_inteval_default = 15 #seconds
image_detection_interval_default = 15 #seconds
sensor_inteval = sensor_inteval_default
image_detection_interval = image_detection_interval_default

def syncConfig(configPayload = ""):
    configValues = []

    if configPayload != "":
        with open('.\\automationConfig.txt', 'w') as cfgFile:
            cfgFile.write(configPayload)

            configValues = configPayload.split(',')

        pass
    else:
        with open('.\\automationConfig.txt', 'r') as cfgFile:
            configFileread = cfgFile.read()
            client.publish("config", configFileread)

            configValues = configFileread.split(',')

    # Config string should have following format: X,X,X,X,X,X
    if len(configValues) == 6:
        global tempLowerBound, tempUpperBound, humidLowerBound, humidUpperBound, lightLowerBound, lightUpperBound
        tempLowerBound = int(configValues[0])
        tempUpperBound = int(configValues[1])
        lightLowerBound = int(configValues[2])
        lightUpperBound = int(configValues[3])
        humidLowerBound = int(configValues[4])
        humidUpperBound = int(configValues[5])
    else:
        print('Invalid automationConfig.txt format. Please check file again!')
        sys.exit()

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    global ser
    print("Feed " + feed_id + " nhan du lieu: " + payload)

    if feed_id == "button1":
        if payload == "0":
            setRelay1(ser, False)
        else:
            setRelay1(ser, True)
    elif feed_id == "button2":
        if payload == "0":
            setRelay2(ser, False)
        else:
            setRelay2(ser, True)
    elif feed_id == "config":
        syncConfig(payload)

def setupModbusSerialConnection(baudrate):
    global usb_port
    usb_port = getPort()

    try:
        ser = serial.Serial(usb_port, baudrate)
        print("Open " + usb_port + " successfully")
        return ser
    except:
        print("Can not open port " + usb_port)
        return ""
    
def setupMQTTConnection():
    global client
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe
    client.connect()
    client.loop_background()

def readSensors(serialConnection):
    global currentTemp, currentLight, currentHumid
    currentTemp = readTemperature(serialConnection)
    currentLight = readLight(serialConnection)
    currentHumid = readMoisture(serialConnection)

def publishSensorData():
    global client
    global currentTemp, currentLight, currentHumid
    client.publish("sensor1", currentTemp)
    client.publish("sensor2", currentLight)
    client.publish("sensor3", currentHumid)


def loadLastConfig():
    if not exists('.\\automationConfig.txt'):
        with open('.\\automationConfig.txt', 'w') as cfgFile:
            cfgFile.write(DEFAULT_AUTOMATION_CONFIG)

    syncConfig()


serialConnection = setupModbusSerialConnection(9600)
setupMQTTConnection()
loadLastConfig()

while True:
    if image_detection_interval <=0:
        image_detection_interval = image_detection_interval_default
        aiResult = image_detector()
        print("Publising AI Result: " + aiResult)
        client.publish("ai", aiResult)

    if sensor_inteval <= 0:
        readSensors(serialConnection)
        publishSensorData()
        
        if currentLight <= lightLowerBound:
            client.publish("button1", "1")
        elif currentLight >= lightUpperBound:
            client.publish("button1", "0")

        if (currentTemp >= tempUpperBound) and (currentHumid <= humidLowerBound):
            client.publish("button2", "1")
        else:
            client.publish("button2", "0")
    
    sensor_inteval -= interval_step
    image_detection_interval -= interval_step

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break
        
    time_elapsed += 1

    if time_out > 0 and time_elapsed == time_out:
        break

    time.sleep(interval_step)


