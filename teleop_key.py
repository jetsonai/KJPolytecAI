import time
import math
import roslibpy
import keyboard

# === 연결 설정 ===
ROS_BRIDGE_IP   = '192.168.90.4'   # 로봇 PC IP로 수정
ROS_BRIDGE_PORT = 9090

# === 속도 한계/스텝 === (원하면 조정)
MAX_LIN = 1.0        # m/s
MAX_ANG = 1.0        # rad/s
STEP_LIN = 0.1       # m/s per step (키를 누르고 있는 동안 0.1초마다 적용)
STEP_ANG = 0.1       # rad/s per step
PUB_HZ   = 10        # 발행 주기 (Hz)

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def main():
    client = roslibpy.Ros(host=ROS_BRIDGE_IP, port=ROS_BRIDGE_PORT)
    print('[teleop] Connecting to rosbridge ws://%s:%d ...' % (ROS_BRIDGE_IP, ROS_BRIDGE_PORT))
    client.run()
    while not client.is_connected:
        time.sleep(0.05)
    print('[teleop] Connected.')

    cmd_vel = roslibpy.Topic(client, '/cmd_vel', 'geometry_msgs/Twist')

    target_lin = 0.0
    target_ang = 0.0
    tick = 0
    try:
        print(
            "\nTeleop (roslibpy)\n"
            "---------------------------------\n"
            "w : linear +   | x : linear -\n"
            "d : angular +  | a : angular -\n"
            "s : STOP (0,0)\n"
            "Ctrl+C to quit\n"
        )

        period = 1.0 / PUB_HZ
        while client.is_connected:
            # === 키 입력 처리 ===
            if keyboard.is_pressed('w'):
                target_lin += STEP_LIN
            if keyboard.is_pressed('x'):
                target_lin -= STEP_LIN
            if keyboard.is_pressed('d'):
                target_ang += STEP_ANG
            if keyboard.is_pressed('a'):
                target_ang -= STEP_ANG
            if keyboard.is_pressed('s'):
                target_lin = 0.0
                target_ang = 0.0

            # 한계 클램핑
            target_lin = clamp(target_lin, -MAX_LIN, MAX_LIN)
            target_ang = clamp(target_ang, -MAX_ANG, MAX_ANG)

            # 메시지 발행
            twist = {
                'linear':  {'x': float(target_lin), 'y': 0.0, 'z': 0.0},
                'angular': {'x': 0.0, 'y': 0.0, 'z': float(target_ang)}
            }
            cmd_vel.publish(roslibpy.Message(twist))

            # 상태 주기적 출력
            tick += 1
            if tick % (PUB_HZ * 1) == 0:  # 1초마다
                print(f"[teleop] lin={target_lin:+.2f} m/s, ang={target_ang:+.2f} rad/s")

            time.sleep(period)

    except KeyboardInterrupt:
        print('\n[teleop] Ctrl+C received.')
    except Exception as e:
        print(f'[teleop] Error: {e}')
    finally:
        # 정지 한번 더 발행
        try:
            cmd_vel.publish(roslibpy.Message({
                'linear':  {'x': 0.0, 'y': 0.0, 'z': 0.0},
                'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
            }))
        except Exception:
            pass
        try:
            cmd_vel.unadvertise()
        except Exception:
            pass
        client.terminate()
        print('[teleop] Disconnected.')

if __name__ == '__main__':
    main()