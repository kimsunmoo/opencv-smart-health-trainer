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
        frame = cv2.resize(frame, dsize=(0, 0), fx=1.5, fy=1.5, interpolation=cv2.INTER_AREA)
        self.height, self.width, _ = frame.shape

        self.ed = exerciseDetector.ExerciseDetector(self.height, self.width)
    
    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, dsize=(0, 0), fx=1.5, fy=1.5, interpolation=cv2.INTER_AREA)
            frame = cv2.flip(frame,1)
            if not ret:
                self.cap.release()
        
            # 선택한 운동에 따라 다르게 처리된 프레임을 받아온다
            if self.setting == constant.EXER_DEFAULT:
                self.frame = frame
            else :
                self.frame = self.ed.detection(frame)
        self.cap.release()

    def getFrame(self):
        return self.frame
    
    # Tkinter의 정보를 받아와서 ed객체로 전달하는 함수
    def setState(self, setting, ex_count):
        self.setting = setting
        self.ed.setState(setting,ex_count)

    # 운동이 완료되었는지 확인하는 함수 (완료 시 기본상태로 초기화)
    def isComplete(self):
        if self.ed.isComplete():
            self.setting = constant.EXER_DEFAULT
            return True