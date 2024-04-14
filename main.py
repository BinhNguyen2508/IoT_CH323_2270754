import sys
import time
from os.path import exists
import cv2
from Adafruit_IO import MQTTClient
# from imageRegconition import *
from plant_disease_ai import *
from rs485 import *

#Demo related variables - START
lightState_demo = False
pumpState_demo = False

temp_demo = 25
humid_demo = 50
light_demo = 20
#Demo related variables - END

AIO_FEED_IDs = ["button1","button2","config"]
AIO_USERNAME = "nbinhsdh222"
AIO_KEY = ""

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
    global lightState_demo, pumpState_demo
    print("Feed " + feed_id + " nhan du lieu: " + payload)
    
    if feed_id == "button1":
        if payload == "0":
            lightState_demo = setRelay1_demo(False)
        else:
            lightState_demo = setRelay1_demo(True)
    elif feed_id == "button2":
        if payload == "0":
            pumpState_demo = setRelay2_demo(False)
        else:
            pumpState_demo = setRelay2_demo(True)
    elif feed_id == "config":
        syncConfig(payload)


port = "/dev/ttyUSB1"
ser = ""
print("Open " + port + " successfully")

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

if not exists('.\\automationConfig.txt'):
    with open('.\\automationConfig.txt', 'w') as cfgFile:
        cfgFile.write('15,45,50,200,20,80') #Default values

syncConfig()

#Set time_out to > 0 to prevent infinite loop
time_out = 300 #seconds
time_elapsed = 0 #seconds

#Loop interval step
interval_step = 1 #seconds

sensor_inteval_default = 15 #seconds
image_detection_interval_default = 15 #seconds
sensor_inteval = sensor_inteval_default
image_detection_interval = image_detection_interval_default

while True:
    if image_detection_interval <=0:
        image_detection_interval_default = 90
        image_detection_interval = image_detection_interval_default
        aiResult = open_file()
        print("Publising AI Result: " + aiResult)
        client.publish("ai", aiResult)

    if sensor_inteval <= 0:
        sensor_inteval = sensor_inteval_default
        temp_demo = readTemperature_demo(temp_demo, pumpState_demo)
        humid_demo = readHumidity_demo(humid_demo, pumpState_demo)
        light_demo = readLight_demo(light_demo, lightState_demo)

        if light_demo >= lightUpperBound:
            lightState_demo = False
        else:
            lightState_demo = True

        if temp_demo <= tempUpperBound and temp_demo >= tempLowerBound and humid_demo >= humidLowerBound and humid_demo <= humidUpperBound:
            pumpState_demo = False
        else:
            pumpState_demo = True
            
        client.publish("button1", str(int(lightState_demo == True)))
        client.publish("button2", str(int(pumpState_demo == True)))
        
        client.publish("sensor1", temp_demo)
        client.publish("sensor3", humid_demo)
        client.publish("sensor2", light_demo)
        
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


