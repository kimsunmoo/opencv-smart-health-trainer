import cv2
import threading

class VideoCap(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.cap = cv2.VideoCapture(0)
    
    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                self.cap.release() 
            self.frame = frame
        self.cap.release()
        print('video capture thread exit')