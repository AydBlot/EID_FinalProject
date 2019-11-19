import cv2
import boto3
import sys
import time
from imutils.video.pivideostream import PiVideoStream
import imutils
import datetime
import uuid
import os
import threading
from threading import Lock 
from videoCamera import VideoCamera
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

#Intialize a client for MQTT
myMQTTClient = AWSIoTMQTTClient("myClientID")

#Create video Camera object
video_camera = VideoCamera(flip=False) # creates a camera object, flip vertically

#teach openCV how to recognize a face with an XML file
object_classifier = cv2.CascadeClassifier("/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

#Initialize the boto3 client to conenct to aws
S3 = boto3.client('s3')

print("Connecting to AWS MQTT Broker...")
# AWS IoT certificate based connection
#myMQTTClient.configureEndpoint("a3aj4aophv141l-ats.iot.us-west-2.amazonaws.com", 8883)
myMQTTClient.configureEndpoint("a3aj4aophv141l-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/EID/finalProject/certs/Amazon_Root_CA_1.pem", "/home/pi/EID/finalProject/certs/7583bb3ead-private.pem.key", "/home/pi/EID/finalProject/certs/7583bb3ead-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(100)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(20)  # 5 sec
myMQTTClient.configureAutoReconnectBackoffTime(1, 128, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)

#connect and publish
myMQTTClient.connect()
print("Successfully Connected to Broker")

def confirm_receive(self, params, packet):
    print("--------new Payload------")
    print("Topic: {} ".format(packet.topic))
    print("Message: {} ".format(packet.payload))

#Subscribe the MQTT client to a topic
myMQTTClient.subscribe("facial/recognition/confirm", 1, confirm_receive)


#Creates a temporary .jpg file in a specified basePath
class TempImage:
    def __init__(self, basePath="/home/pi/images", ext=".jpg"):

        # construct the file path
        
        self.key = "{rand}{ext}".format(rand=str(uuid.uuid4()), ext=ext)
        self.path = "{base_path}/{key}".format(base_path=basePath,key=self.key)    
 
    def cleanup(self):
		# remove the file
        os.remove(self.path)

SOURCE_FILENAME = '/home/pi/images/test.jpg'
NEW_FACE_BUCKET_NAME = 'facialrecnewfacebucket'

def check_for_face():
    image_delay_time = 0
    while True:
        try:
            _, found_face, frame = video_camera.get_object(object_classifier)
            if found_face and (time.time() - image_delay_time) > 3:
                print(time.time() - image_delay_time)
                print("Face Recognized")
                status = cv2.imwrite('/home/pi/images/test.jpg', frame)
                print("Image written to file-system : ",status)
                t = TempImage()
                print(t.path)
                cv2.imwrite(t.path, frame)
                S3.upload_file(t.path, NEW_FACE_BUCKET_NAME, t.path)
                #Update the read permissions so the lambda function can access the newly added s3 object
                os.system("aws s3api put-object-acl --bucket {0} --key {1} --acl public-read".format(NEW_FACE_BUCKET_NAME, t.path))
                image_delay_time = time.time()
        except:
            print("camera object not working:", sys.exc_info()[0])

if __name__ == '__main__':
    check_for_face()
