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

#Create video Camera object
video_camera = VideoCamera(flip=False) # creates a camera object, flip vertically

#teach openCV how to recognize a face with an XML file
object_classifier = cv2.CascadeClassifier("/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
image_delay_time = 0
#Initialize the boto3 client to conenct to aws
S3 = boto3.client('s3')

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
    global image_delay_time
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
                image_delay_time = time.time()
        except:
            print("camera object not working:", sys.exc_info()[0])

if __name__ == '__main__':
    check_for_face()
