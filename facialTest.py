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

video_camera = VideoCamera(flip=False) # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

class TempImage:
    def __init__(self, basePath="images", ext=".jpg"):

        # construct the file path
        
        self.key = "{rand}{ext}".format(rand=str(uuid.uuid4()), ext=ext)
        self.path = "{base_path}/{key}".format(base_path=basePath,key=self.key)    
 
    def cleanup(self):
		# remove the file
        os.remove(self.path)

S3 = boto3.client('s3')
SOURCE_FILENAME = 'selfie.jpg'
BUCKET_NAME = 'aydblotfacialrecbucket'

def check_for_face():
    while True:
        try:
            _, found_face, frame = video_camera.get_object(object_classifier)
            print("found face:{}", found_face)
            if found_face:
                print("Face Recognized")
                t = TempImage()
                cv2.imwrite(t.path, frame)
                S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, SOURCE_FILENAME)

        except:
            print("camera object not working:", sys.exc_info()[0])
if __name__ == '__main__':
    check_for_face()
