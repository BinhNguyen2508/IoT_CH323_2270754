import random
import sys
import time
import cv2
from Adafruit_IO import MQTTClient
from imageRegconition import *
from rs485 import *

AIO_FEED_IDs = ["button1","button2"]
AIO_USERNAME = "nbinhsdh222"
AIO_KEY = "aio_rkwN72PzDsGXHWWKQaouwGq0EibK"

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

    if feed_id == "button1":
        if payload == "0":
            setRelay3(ser, True)
        else:
            setRelay3(ser, False)
    # elif feed_id == "button2":
    #     if payload == "0":
    #         writeData(3)
    #     else:
    #         writeData(4)

port = getPort()

try:
    ser = serial.Serial(port, baudrate=9600)
    print("Open " + port + " successfully")
except:
    print("Can not open port " + port)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

interval_step = 1 #seconds
time_out = 150 #seconds
time_elapsed = 0 #seconds

# random_interval_default = 15 #seconds
# image_detection_interval_default = random_interval_default

# random_interval = random_interval_default 
# image_detection_interval = image_detection_interval_default

while True:
    # if random_interval <= 0:
    #     random_interval = random_interval_default
    #     print("Random data is publishing..." )
    #     temperature = random.randint(15,60)
    #     client.publish("sensor1", temperature)
    #     lumen = random.randint(0,100)
    #     client.publish("sensor2", lumen)
    #     humidity = random.randint(0,100)
    #     client.publish("sensor3", humidity)

    # if image_detection_interval <=0:
    #     print("Image data is publising...")
    #     image_detection_interval = image_detection_interval_default
    #     imageDetectionResult = imageDetection()
    #     client.publish("ai", imageDetectionResult)
        
    # random_interval = random_interval - interval_step
    # image_detection_interval = image_detection_interval - interval_step

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break
        
    # readSerial(client)
    time_elapsed = time_elapsed + 1

    if time_elapsed == time_out:
        break

    time.sleep(interval_step)


