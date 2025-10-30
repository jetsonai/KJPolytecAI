import roslibpy
import time

# WSL2의 IP 주소와 포트 번호
# WSL2의 IP 주소 또는 localhost를 사용할 수 있습니다.
client = roslibpy.Ros(host='10.230.38.97', port=9090)
client.run()

print('ROS 연결 중...')

if client.is_connected:
    print('ROS 연결 성공!')

    # 토픽 발행 예제
    talker = roslibpy.Topic(client, '/chatter', 'std_msgs/String')
    i = 0
    while client.is_connected:
        message = roslibpy.Message({'data': f'hello roslibpy from windows: {i}'})
        talker.publish(message)
        print(f'메시지 발행: {message["data"]}')
        i += 1
        time.sleep(1)

client.terminate()