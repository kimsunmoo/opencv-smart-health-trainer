EXER_DEFAULT = -1
EXER_SQUAT = 0
EXER_DUMBBELL_CURL_R = 1
EXER_DUMBBELL_CURL_L = 2

#이미지 경로 리스트
IMAGE_FILES = ["img/SQUAT.png", "img/DUMBBELL_CURL_R.png", "img/DUMBBELL_CURL_L.png"]

#ANGLES
#[0] : 미는 운동 = 0, 당기는 운동 = 1
#[1] : up 경계 각도
#[2] : down 경계 각도
#[3], [4] : 부상 위험 각도
ANGLES = [
    [0, 160, 90, 180, 45],
    [1, 45, 160, 170, 10]
]