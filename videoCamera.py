#utilized code from just4give/home-surveillance github repo as basis for code
import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import datetime
import json

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.vs.camera.rotation=270
        self.flip = flip
        self.vs.framerate=10
        self.vs.resolution=90
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame
    
    #Grab an image and rotate to ensure it is in the proper orientation
    def get_object(self, classifier):
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S.%f%p")
        found_objects = False
        frame = self.flip_if_needed(self.vs.read()).copy() 
        newframe = imutils.rotate(frame, -90)
        #img = cv2.imread('photo-1507003211169-0a1dd7228f2d.jpg')
        gray = cv2.cvtColor(newframe, cv2.COLOR_BGR2GRAY)

        objects = classifier.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30))

        if len(objects) > 0:
            found_objects = True
            

        # Draw a rectangle around the objects
        for (x, y, w, h) in objects:
            frame2 = cv2.rectangle(newframe, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #t = TempImage()
            #t.cleanup()

        cv2.putText(frame,ts,(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 255, 0), 1)
        #cv2.imshow("feed",frame)
        #cv2.waitKey(1000)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes(), found_objects, newframe)
