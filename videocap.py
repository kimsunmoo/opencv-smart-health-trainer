import cv2
import threading
import exerciseDetector
import constant

class VideoCap(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.setting = constant.EXER_SQUAT
        self.cap = cv2.VideoCapture(0)

        self.ed = exerciseDetector.ExerciseDetector()
    
    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                self.cap.release()
            if self.setting == constant.EXER_DEFAULT:
                self.frame = frame
            else :
                self.frame = self.ed.detection(frame)
        self.cap.release()
        print('video capture thread exit')