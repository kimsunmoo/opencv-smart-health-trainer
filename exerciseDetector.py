#참고한 자료 : https://github.com/nicknochnack/MediaPipePoseEstimation
import cv2
import mediapipe as mp
import numpy as np
import threading

import constant

class ExerciseDetector():
    def __init__(self, height, width):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.height = height
        self.width = width

        # 부상위험이 있을 때 화면을 붉게 만드는 필터
        self.red_filter = np.full((self.height ,self.width, 3), (0, 0, 100), dtype=np.uint8)
        
        self.counter = 0
        # stage : 현재 동작의 상태를 나타내는 변수
        self.stage = None
        # warn : 부상위험을 나타내는 변수
        self.warn = False

        self.setting = constant.EXER_DEFAULT
        self.ex_count = 0

        # 처리가 완료되지 않은 이미지를 참조하지 않도록 함
        self.lock = threading.Lock()

    def detection(self, frame):
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Make detection
        results = self.pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            a, b, c = self.getCoordinates(landmarks)

            # Calculate angle
            angle = self.calculate_angle(a, b, c)

            # Visualize angle
            cv2.putText(image, str(angle),
                        tuple(np.multiply(b, [self.width, self.height]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )
            self.updateStates(angle)
        except:
            pass
        
        # 부상 위험이 있을 때 필터 적용
        if self.warn:
            image = cv2.add(image, self.red_filter)
        

        # 운동의 가이드라인을 frame에 붙인다
        self.lock.acquire
        image = cv2.add(image, self.guide)
        self.lock.release
        
        # Setup status box
        cv2.rectangle(image, (0, 0), (300, 73), (245, 117, 16), -1)
        cv2.putText(image, 'REPS', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(self.counter),
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        # Stage data
        cv2.putText(image, 'STAGE', (120, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, self.stage,
                    (120, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        # Render detections
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                )

        return image

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle
        
        angle = int(angle)

        return angle

    # 각 운동에 따라 필요한 관절의 좌표 정보를 return 하는 함수
    # 거울 반전이 되어 있어 오른쪽/왼쪽 반대로 적용
    def getCoordinates(self, landmarks):
        if self.setting==constant.EXER_SQUAT:
            a = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            b = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            c = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                    landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        elif self.setting==constant.EXER_DUMBBELL_CURL_R:
            a = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            b = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                    landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            c = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                    landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        elif self.setting==constant.EXER_DUMBBELL_CURL_L:
            a = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            b = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                    landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            c = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                    landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        return (a, b, c)

    #각도에 따라 stage를 변경하고 개수를 카운트 함 
    def updateStates(self, angle):
        angles = constant.ANGLES[self.setting]
        
        #미는 운동
        if angles[0] == 0:
            if angle > angles[1]:
                self.stage = "up"
            if angle < angles[2] and self.stage == "up":
                self.stage = "down"
                self.counter += 1
        
        #당기는 운동
        else :
            if angle > angles[2]:
                self.stage = "down"
            if angle < angles[1] and self.stage == "down":
                self.stage = "up"
                self.counter += 1

        #constant.py  10 ~ 14 라인 참조
        if angle < angles[3] and angle > angles[4]:
            self.warn = False
        else:
            self.warn = True

    #운동 정보를 업데이트 하는 함수
    def setState(self, setting, ex_count):
        self.setting = setting
        self.ex_count = ex_count
        self.counter = 0

        if setting != -1:
            self.lock.acquire
            self.guide = cv2.imread(constant.IMAGE_FILES[setting])
            self.guide = cv2.resize(self.guide, dsize=(self.width, self.height), interpolation=cv2.INTER_AREA)
            self.lock.release

    #운동이 완료되었는지 판단 후 변수 초기화
    def isComplete(self):
        if self.ex_count == self.counter and self.ex_count != 0:
            self.counter = 0
            self.stage = None
            return True

    def __exit__(self):
        self.pose.close()