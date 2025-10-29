# KJPolytecAI

## 1. 알쌤 로봇 기본 기능 앱

터미널을 열고

./testapp.py

## 2. OpenCV + 카메라 실습

cd

cd opencv_start

### OpenCV 이미지 파일 보기

python3 01_eximage.py

### OpenCV 비디오 파일 보기

python3 02_exvideo.py

### OpenCV 카메라 보기

python3 03_camera.py

## 3. MediaPipe + 카메라 실습

cd

cd GestureControlEx/

### MediaPipe 자세 추정

python3 PoseEstimation/Basics.py

### MediaPipe 얼굴 메쉬

python3 FaceMesh/Basics.py

### MediaPipe 눈 깜박임 카운트

python3 EyeBlinkCounter/EyeBlinkCounter.py

### MediaPipe 손가락 카운트

python3 FingerCount/FingerCounter.py

### MediaPipe 드래그 앤 드랍 실습

python3 DragandDrop/DragandDrop_usb.py


## 4. ROS + 모터제어 실습

모터 준비

roslaunch ros_aibot_core aibot_core_ready.launch

### 전진

rosrun ros_aibot_core aibot_ctl_pub 0

   전진하면 Ctl-C

### 정지

rosrun ros_aibot_core aibot_ctl_pub 5

   정지하면 Ctl-C

### 우회전

rosrun ros_aibot_core aibot_ctl_pub 3

   우회전하면 Ctl-C
   
### 좌회전

rosrun ros_aibot_core aibot_ctl_pub 4

   좌회전하면 Ctl-C

## 5. ROS + 원격 제어 실습

모터 준비

roslaunch ros_aibot_core aibot_core_ready.launch

