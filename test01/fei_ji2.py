from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative,Attitude
from Photo import photo,photo_again_operation
from pymavlink import mavutil


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
    Attitude(0, 0, jiao)
    # 飞过去留10米
    tm = (dst - 5) // 2
    print("go")
    send_body_ned_velocity(0, 2, 0, 10)
    time.sleep(tm)

    # 拍照操作
    photo_again_operation()

    # 倒飞回来
    print("back")
    send_body_ned_velocity(0, -2, 0, 10)
    time.sleep(tm)
    # 角转回来
    Attitude(0, 0, -jiao)

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


connection_string = '10.42.0.10:14550'
print('Connecting to vehicle on: %s' % connection_string)

vehicle = connect(connection_string, wait_ready=True, baud=921600)

arm_and_takeoff(10)

# -------------------------------------------------------------------------------------------------------

print("Set default/target airspeed to 3")
vehicle.airspeed = 2

info = False
dst = 10
jiao = 60

si_xun_huan = 4

# 飞行死循环
while si_xun_huan > 0:
    # 左转90度
    Attitude(0, 0, -90)
    # 飞100米
    send_body_ned_velocity_gai_zao(0, 2, 0, 10)
    si_xun_huan += 1
    



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
无人机执行的任务大致如下：

1. **起飞**：
   - 无人机解锁并起飞到10米的高度。

2. **设置空速**：
   - 设置无人机的默认空速为2米/秒。

3. **循环飞行和拍照**：
   - 无人机进入一个循环，每次循环包括：
     - 调整姿态，左转90度。
     - 向前飞行一段距离（速度为2米/秒，持续10秒）。
     - 在飞行过程中，`send_body_ned_velocity_gai_zao`函数会调用`photo`函数检查是否需要拍照，并根据返回的信息决定是否执行`go_and_back`操作。这意味着无人机会飞到一个预设的点，进行拍照，然后返回原点或转向下一个点。

4. **返航降落**：
   - 完成所有循环后，无人机将执行返航操作，自动返回起飞点并降落。

5. **关闭连接**：
   - 在无人机开始返航后，关闭与无人机的连接。

简而言之，无人机的任务是飞到多个点进行拍照，每次拍照后返回或转向下一个点，直到完成所有预定的拍照点后返回起飞点并降落。这种模式通常用于巡查、监测或搜索任务，其中需要在多个位置收集图像数据。
'''
'''
拍照的决策是由 photo 函数来决定的。这个函数可能包含一些逻辑来确定是否当前的条件适合拍照。虽然具体的实现细节没有在代码中给出，但通常这样的函数会考虑以下几个因素：

位置：

无人机是否已经到达了预设的拍照点。
高度：

无人机是否已经达到适合拍照的高度。
稳定性：

无人机是否处于稳定的状态，没有剧烈的摇晃或移动，以确保照片质量。
环境条件：

光照条件是否充足，或者是否在预定的环境条件下（例如，没有过多的遮挡物）。
目标检测：

是否在相机视野内检测到了需要拍摄的目标或特定特征。
电量：

无人机的电量是否足够支持继续飞行和拍照。
存储空间：

无人机的存储设备是否有足够的空间来保存新的照片。
在代码的 send_body_ned_velocity_gai_zao 函数中，无人机在向前飞行的过程中会持续检查这些条件，一旦 photo 函数返回表示可以拍照的信息，无人机就会执行 go_and_back 函数来进行拍照操作。这通常涉及到飞到一个点，执行拍照，然后返回或飞往下一个点。

例如，photo 函数可能会返回一个布尔值或包含信息的对象，如果返回值为真（True），则表示当前条件适合拍照，随后会调用 photo_again_operation 函数来执行拍照动作。如果拍照成功或有必要的信息被捕捉，无人机将继续执行后续的飞行和拍照任务。


'''