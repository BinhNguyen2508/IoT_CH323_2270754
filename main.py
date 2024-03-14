import random
import sys
import time
import cv2  # Install opencv-python
from Adafruit_IO import MQTTClient
from imageRegconition import *

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

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

interval_step = 1 #seconds

random_interval_default = 15 #seconds
image_detection_interval_default = random_interval_default

random_interval = random_interval_default 
image_detection_interval = image_detection_interval_default

while True:
    if random_interval <= 0:
        random_interval = random_interval_default
        print("Random data is publishing..." )
        temperature = random.randint(15,60)
        client.publish("sensor1", temperature)
        lumen = random.randint(0,100)
        client.publish("sensor2", lumen)
        humidity = random.randint(0,100)
        client.publish("sensor3", humidity)

    if image_detection_interval <=0:
        print("Image data is publising...")
        image_detection_interval = image_detection_interval_default
        imageDetectionResult = imageDetection()
        client.publish("ai", imageDetectionResult)
        
    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break
        
    time.sleep(interval_step)
    random_interval = random_interval - interval_step
    image_detection_interval = image_detection_interval - interval_step

