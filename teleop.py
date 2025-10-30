import roslibpy
import time
import keyboard

# 1. 로봇 PC의 IP 주소와 rosbridge 포트를 설정합니다.
ROS_BRIDGE_IP = '192.168.90.4' # 로봇 PC의 IP 주소로 변경하세요.
ROS_BRIDGE_PORT = 9090

# 2. 로스브릿지 연결
client = roslibpy.Ros(host=ROS_BRIDGE_IP, port=ROS_BRIDGE_PORT)

try:
    print("ROS 연결 시도...")
    client.run()
    print("ROS 연결 성공")

    # 3. 'cmd_vel' 토픽에 대한 발행자(publisher) 생성
    # 메시지 타입은 'geometry_msgs/Twist'입니다.
    cmd_vel_topic = roslibpy.Topic(client, '/cmd_vel', 'geometry_msgs/Twist')

    print("키보드 텔레오퍼레이션 시작.")
    print("위/아래: 전/후진")
    print("왼쪽/오른쪽: 좌/우 회전")
    print("스페이스바: 정지")
    print("Ctrl+C로 종료")

    linear_speed = 0.5  # 선속도
    angular_speed = 1.0 # 각속도
    
    while client.is_connected:
        twist = roslibpy.Message({'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}})
        twist['linear']['x'] = 0
        if keyboard.is_pressed('w'):
            twist['linear']['x'] = linear_speed
        elif keyboard.is_pressed('x'):
            twist['linear']['x'] = -linear_speed

        if keyboard.is_pressed('left'):
            twist['angular']['z'] = angular_speed
        elif keyboard.is_pressed('right'):
            twist['angular']['z'] = -angular_speed

        # 스페이스바를 누르면 정지
        if keyboard.is_pressed('space'):
            twist['linear']['x'] = 0.0
            twist['angular']['z'] = 0.0

        # 4. Twist 메시지 발행
        cmd_vel_topic.publish(twist)
        time.sleep(0.1) # 100ms 간격으로 메시지 발행

except roslibpy.core.RosTimeoutError:
    print("ROS 연결 시간 초과.")
except Exception as e:
    print(f"오류 발생: {e}")
finally:
    # 5. 연결 종료
    if client.is_connected:
        print("연결 종료 중...")
        client.terminate()
        print("연결 종료됨.")
