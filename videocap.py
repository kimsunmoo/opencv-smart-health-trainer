import cv2
import threading
import exerciseDetector
import constant

class VideoCap(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.setting = constant.EXER_DEFAULT
        self.cap = cv2.VideoCapture(0)

        ret, frame = self.cap.read()
        self.height, self.width, _ = frame.shape
        self.height = int(self.height * 1.5)
        self.width = int(self.width * 1.5)

        self.ed = exerciseDetector.ExerciseDetector(self.height, self.width)
    
    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, dsize=(0, 0), fx=1.5, fy=1.5, interpolation=cv2.INTER_AREA)
            frame = cv2.flip(frame,1)
            if not ret:
                self.cap.release()
            if self.setting == constant.EXER_DEFAULT:
                self.frame = frame
            else :
                self.frame = self.ed.detection(frame)
        self.cap.release()
        print('video capture thread exit')

    def getFrame(self):
        return self.frame
        
    def setState(self, setting, ex_count):
        self.setting = setting
        self.ed.setState(setting,ex_count)