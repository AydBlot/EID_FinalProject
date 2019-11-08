import cv2
from camera import Videocamera
video_camera = VideoCamera(flip=False) # creates camera object
object_classifier = cv2.CascadeClassifier("models/haarcascade_frontalface_alt.xml")

                #try:
                #_, found_face, frame = video_camera.get_object(object_classifier)
                #if found_face:
def check_for_face():
    while True:
        video_capture = cv2.VideoCapture(0)
        if (video_capture.isOpened() == False):
            print("Error opening video stream")
        while (video_capture.isOpened()):
            ret, frame = video_capture.read()
            if ret == True:
                cv2.imshow('Frame', frame)

            if cv2.waitkey(25) & 0xFF == ord('q'):
                break
            else:
                break

        video_capture.release()
        cv2.destroyAllWindows()
if __name__ == '__main__':
    check_for_face()
