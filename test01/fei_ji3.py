from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative,Attitude,Gimbal
from Photo import photo,photo_again_operation
from pymavlink import mavutil
import cv2 as cv

def arm_and_takeoff(aTargetAltitude):
    # 进行起飞前检查  
    print("Basic pre-arm checks")
    # vehicle.is_armable会检查飞控是否启动完成、有无GPS fix、卡曼滤波器  
    # 是否初始化完毕。若以上检查通过，则会返回True  
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    # 解锁无人机（电机将开始旋转）  
    print("Arming motors")
    # 将无人机的飞行模式切换成"GUIDED"（一般建议在GUIDED模式下控制无人机）  
    vehicle.mode = VehicleMode("GUIDED")
    # 通过设置vehicle.armed状态变量为True，解锁无人机  
    vehicle.armed = True

    # 在无人机起飞之前，确认电机已经解锁  
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    # 发送起飞指令  
    print("Taking off!")
    # simple_takeoff将发送指令，使无人机起飞并上升到目标高度  
    vehicle.simple_takeoff(aTargetAltitude)

    # 在无人机上升到目标高度之前，阻塞程序  
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # 当高度上升到目标高度的0.95倍时，即认为达到了目标高度，退出循环  
        # vehicle.location.global_relative_frame.alt为相对于home点的高度  
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        # 等待1s  
        time.sleep(1)




# 飞过去操作，并且飞回来
def go_and_back():
    # 转角
    vehicle.gimbal.rotate(0, 0, jiao)
    # 飞过去留10米
    tm = (dst - 5) // 10
    print("go")
    send_body_ned_velocity(2, 0, 0, 10)
    time.sleep(tm)

    # 拍照操作
    photo_again_operation()

    # 倒飞回来
    print("back")
    send_body_ned_velocity(-2, 0, 0, 10)
    time.sleep(tm)
    # 角转回来
    vehicle.gimbal.rotate(0, 0, -jiao)

# 飞行函数
def send_body_ned_velocity_gai_zao(velocity_x, velocity_y, velocity_z, duration=0):
    global dst,jiao
    print("patrolling")
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,  # time_boot_ms (not used)
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED,  # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
        0b0000111111000111,  # type_mask
        0, 0, 0,  # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z,  # m/s
        0, 0, 0,  # x, y, z acceleration
        0, 0)
    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

        info, dst, jiao = photo()
        if not info: continue
        else: go_and_back() # 过去检测


# 飞行函数
def send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration=0):
    print("Going back and forth between monitoring points and patrols")
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
        0b0000111111000111, # type_mask
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # m/s
        0, 0, 0, # x, y, z acceleration
        0, 0)
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)


connection_string = '/dev/ttyUSB0'
print('Connecting to vehicle on: %s' % connection_string)

vehicle = connect(connection_string, wait_ready=True, baud=921600)

# -------------------------------------------------------------------------------------------------------

print("Set default/target airspeed to 3")

print(vehicle.attitude.yaw)
print(vehicle.location.global_relative_frame)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")

# -------------------------------------------------------------------------------------------------------

# 发送"返航"指令  
print("Returning to Launch")
# 返航，只需将无人机的飞行模式切换成"RTL(Return to Launch)"  
# 无人机会自动返回home点的正上方，之后自动降落  
vehicle.mode = VehicleMode("RTL")

# 退出之前，清除vehicle对象  
print("Close vehicle object")
vehicle.close()

'''
photo函数：用于检测是否应该拍照，并返回拍照所需的信息（如位置、角度）。
photo_again_operation函数：用于执行实际的拍照操作(等待完成）。
无人机的具体执行流程如下：

连接到无人机。
起飞到指定高度。
进入主循环，执行飞行任务：
向前飞行并检查是否需要拍照。
如果需要，执行拍照操作并返回原点。
完成所有任务后，执行返航降落操作。
关闭与无人机的连接。

加yolo
'''