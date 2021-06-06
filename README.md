# opencv-Smart-Health-Trainer
opencv 텀 프로젝트

# 프로그램 구성
main.py : 프로그램을 작동 시키는 파일로써 ui.py, videoCap.py, exerciseDetector.py를 연결시켜주는 역할을 한다.

ui.py : tkinter 화면을 구성하는 클래스 

videoCap.py : 웹캠으로부터 영상을 읽어와서 선택한 운동에 따라 영상을 다르게 처리하는 클래스

exerciseDetector.py : mediapipe를 사용하여 운동과정을 보조해주는 클래스 (부상 방지, 운동 횟수 카운트, 가이드 라인 제공)

constant.py : 운동 종류와 각도에 대한 상수값을 정의한 파일


# 실행환경 구축
Python 설치 필요 3.7 이상 사용 권장

Opencv 설치

$ pip install opencv-python

Mediapipe 설치

$ pip install mediapipe

Pillow 설치

$ pip install pillow

# 참고 자료
Opencv : https://github.com/opencv/opencv

Mediapipe : https://google.github.io/mediapipe/

Mediapipe 검출 방법 : https://github.com/nicknochnack/MediaPipePoseEstimation
