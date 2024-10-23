#!/usr/bin/env python  
# -*- coding: utf-8 -*-  

""" 
© Copyright 2015-2016, 3D Robotics. 
simple_goto.py: GUIDED mode "simple goto" example (Copter Only) 
Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto. 
"""

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

# 改为当前连接的pixhawk飞控的端口 
connection_string = '/dev/ttyUSB0'
print('Connecting to vehicle on: %s' % connection_string)
# connect函数将会返回一个Vehicle类型的对象，即此处的vehicle  
# 即可认为是无人机的主体，通过vehicle对象，我们可以直接控制无人机  
vehicle = connect(connection_string,wait_ready=True,baud=921600)

# 定义arm_and_takeoff函数，使无人机解锁并起飞到目标高度  
# 参数aTargetAltitude即为目标高度，单位为米  
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

# 调用上面声明的arm_and_takeoff函数，目标高度3m  
arm_and_takeoff(3)

# 设置在运动时，默认的空速为3m/s  
print("Set default/target airspeed to 3")
# vehicle.airspeed变量可读可写，且读、写时的含义不同。  
# 读取时，为无人机的当前空速；写入时，设定无人机在执行航点任务时的默认速度  
vehicle.airspeed = 3

#定义方向控制
def send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration=0):
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

# 让无人机向左飞行,速度0.2m/s,飞行时间(duration)10秒,延迟(sleep)2秒这样拐角更方正.
# x表示前后方向,y表示左右方向,z表示垂直高度方向
velocity_x = 0
velocity_y = -0.2
velocity_z = 0
duration = 10
send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration)
time.sleep(2)

#让无人机向前飞行,速度0.2m/s,飞行时间10秒
velocity_x = 0.2
velocity_y = 0
velocity_z = 0
duration = 10
send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration)
time.sleep(2)

#也可以用下面这种格式:让无人机向右飞行,速度0.2m/s,飞行时间10秒
send_body_ned_velocity(0,0.2,0,10)
time.sleep(2)

#最后让无人机向后飞行,速度0.2m/s,飞行时间5秒,这样无人机就飞出一个正方形
send_body_ned_velocity(-0.2,0,0,10)
time.sleep(2)
# 发送"降落"指令  
print("Land")
# 降落，只需将无人机的飞行模式切换成"Land"  
# 无人机会自动返回home点的正上方，之后自动降落  
vehicle.mode = VehicleMode("LAND")

# 退出之前，清除vehicle对象  
print("Close vehicle object")
vehicle.close()
