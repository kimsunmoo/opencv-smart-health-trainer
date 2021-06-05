import cv2
import mediapipe as mp
import numpy as np
import numpy as np
import constant

class ExerciseDetector():
    def __init__(self, height, width):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.height = height
        self.width = width

        self.red_filter = np.full((self.height ,self.width, 3), (0, 0, 100), dtype=np.uint8)
        
        self.counter = 0
        self.stage = None
        self.warn = False

        self.setting = constant.EXER_SQUAT
        self.ex_countb = 0

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
                        tuple(np.multiply(b, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )
            self.updateStates(angle)
        except:
            pass
        # Render curl counter
        # Setup status box
        if self.warn:
            image = cv2.add(image, self.red_filter)
        image = cv2.add(image, self.guide)
        cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
        cv2.putText(image, 'REPS', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(self.counter),
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        # Stage data
        cv2.putText(image, 'STAGE', (65, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, self.stage,
                    (60, 60),
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

        return angle

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

    def updateStates(self, angle):
        angles = constant.ANGLES[self.setting]
        if angles[0] == 0:
            if angle > angles[1]:
                self.stage = "up"
            if angle < angles[2] and self.stage == "up":
                self.stage = "down"
                self.counter += 1
                print(self.counter)
        else :
            if angle > angles[2]:
                self.stage = "down"
            if angle < angles[1] and self.stage == "down":
                self.stage = "up"
                self.counter += 1
                print(self.counter)

        if angle < angles[3] and angle > angles[4]:
            self.warn = False
        else:
            self.warn = True

    def setState(self, setting, ex_count):
        self.setting = setting
        self.ex_count = ex_count

        self.guide = cv2.imread(constant.IMAGE_FILES[setting])
        self.guide = cv2.resize(self.guide, dsize=(self.width, self.height), interpolation=cv2.INTER_AREA)

    def __exit__(self):
        self.pose.close()