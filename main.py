import sys
import time
from os.path import exists
import cv2
from Adafruit_IO import MQTTClient
# from imageRegconition import *
from plant_disease_ai import *
from rs485 import *

#Demo related variables - START
isDemo = 1

lightState_demo = False
pumpState_demo = False

temp_demo = 25
humid_demo = 50
light_demo = 20
#Demo related variables - END

global AIO_FEED_IDs
isFirstTimeConfig = False

if isDemo:
    #Light - button1; Pump - button2;
    AIO_FEED_IDs = ["button1","button2"]
    pass
else:
    AIO_FEED_IDs = ["button1","button2","cfg_tempL","cfg_tempU","cfg_humidL","cfg_humidU","cfg_lightL","cfg_lightU"] #Light - button1; Pump - button2
    pass

AIO_USERNAME = "nbinhsdh222"
AIO_KEY = ""

global port, ser
global tempLowerBound, tempUpperBound
global humidLowerBound, humidUpperBound
global lightLowerBound, lightUpperBound

if exists('.\\automationConfig.txt'):
    with open('.\\automationConfig.txt', 'r') as cfgFile:
        configuration = cfgFile.read()
        configValues = configuration.split(',')

        # Config string should have following format: X,X,X,X,X,X
        if len(configValues) == 6:
            tempLowerBound = int(configValues[0])
            tempUpperBound = int(configValues[1])
            lightLowerBound = int(configValues[2])
            lightUpperBound = int(configValues[3])
            humidLowerBound = int(configValues[4])
            humidUpperBound = int(configValues[5])
        else:
            print('Invalid automationConfig.txt format. Please check file again!')
            sys.exit()
else:
    with open('.\\automationConfig.txt', 'w') as cfgFile:
        cfgFile.write('15,45,50,200,20,80') #Default values
        
    isFirstTimeConfig = True

if isDemo:
    port = "/dev/ttyUSB1"
    ser = ""
    print("Open " + port + " successfully")
    pass
else:
    port = getPort()

    try:
        ser = serial.Serial(port, baudrate=9600)
        print("Open " + port + " successfully")
    except:
        print("Can not open port " + port)
    pass

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
    print("Feed " + feed_id + " nhan du lieu: " + payload)

    if isDemo:
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
    else:
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
        pass

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

if isFirstTimeConfig and not isDemo:
    client.publish("cfg_tempL", str(tempLowerBound))
    client.publish("cfg_tempU", str(tempUpperBound))
    client.publish("cfg_lightL", str(humidLowerBound))
    client.publish("cfg_lightU", str(humidUpperBound))
    client.publish("cfg_humidL", str(lightLowerBound))
    client.publish("cfg_humidU", str(lightUpperBound))

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
        if isDemo:
            image_detection_interval_default = 90
            image_detection_interval = image_detection_interval_default
            aiResult = open_file()
            print("Publising AI Result: " + aiResult)
            client.publish("ai", aiResult)
        else:
            image_detection_interval = image_detection_interval_default
            aiResult = image_detector()
            print("Publising AI Result: " + aiResult)
            client.publish("ai", aiResult)

    if sensor_inteval <= 0:
        if isDemo:
            sensor_inteval = sensor_inteval_default
            temp_demo = readTemperature_demo(temp_demo, pumpState_demo)
            humid_demo = readHumidity_demo(humid_demo, pumpState_demo)
            light_demo = readLight_demo(light_demo, lightState_demo)

            if light_demo >= 200:
                lightState_demo = False
            else:
                lightState_demo = True

            if temp_demo <= 25 and humid_demo >= 60:
                pumpState_demo = False
            else:
                pumpState_demo = True
                
            client.publish("button1", str(int(lightState_demo == True)))
            client.publish("button2", str(int(pumpState_demo == True)))
            
            client.publish("sensor1", temp_demo)
            client.publish("sensor3", humid_demo)
            client.publish("sensor2", light_demo)
        else:
            currentTemp = readTemperature(ser)
            currentLight = readLight(ser)
            currentHumid = readMoisture(ser)

            client.publish("sensor1", currentTemp)
            client.publish("sensor2", currentLight)
            client.publish("sensor3", currentHumid)
            
            if currentLight <= lightLowerBound:
                client.publish("button1", "1")
            elif currentLight >= lightUpperBound:
                client.publish("button1", "0")

            if (currentTemp >= tempLowerBound and currentTemp <= tempUpperBound) and (currentHumid >= humidLowerBound and currentHumid <= humidUpperBound):
                client.publish("button2", "0")
            else:
                client.publish("button2", "1")
        pass
        
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


