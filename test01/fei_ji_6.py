from __future__ import print_function

import math
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from Photo import photo, photo_again_operation, thread_for_shi_pin
from pymavlink import mavutil
# from s2022_10_29_for_debug import thread_for_shi_pin
import input_gol
import cv2 as cv
import threading


# -------------------------------------------------------------------------------------------------------
class fei_ji():
    def __init__(self):
        connection_string = '/dev/ttyUSB0'
        print('Connecting to vehicle on: %s' % connection_string)
        self.vehicle = connect(connection_string, wait_ready=True, baud=921600)
        # 起飞
        self.arm_and_takeoff(10)

        print("Set default/target airspeed to 3")
        self.vehicle.airspeed = 3

        self.info = False
        self.dst = 10
        self.jiao = 60
        self.si_xun_huan = 0
        self.LocationGlobalRelativeList = []
        self.read_location()
        # 初始化摄像头
        self.cap = cv.VideoCapture(0)

    def __del__(self):
        # 发送"返航"指令
        print("Returning to Launch")
        # 返航，只需将无人机的飞行模式切换成"RTL(Return to Launch)"
        # 无人机会自动返回home点的正上方，之后自动降落
        self.vehicle.mode = VehicleMode("RTL")
        # 退出之前，清除vehicle对象
        print("Close vehicle object")
        self.vehicle.close()
        # 释放摄像头资源
        self.cap.release()
        cv.destroyAllWindows()

    def __is_i(self, i: LocationGlobalRelative) -> bool:
        if (
                (self.my_round(self.vehicle.location.global_relative_frame.lon, 4) == self.my_round(i.lon, 4)) and
                (self.my_round(self.vehicle.location.global_relative_frame.lat, 4) == self.my_round(i.lat, 4))
        ):
            return True
        else:
            return False

    def my_round(self, number, beilv):
        zong = math.pow(10, beilv)
        return int(number * zong) / zong

    def start(self):
        thread_for_shi_pin(10)
        # 创建并启动实时识别线程
        recognition_thread = threading.Thread(target=self.real_time_recognition)
        recognition_thread.start()
        for i in self.LocationGlobalRelativeList:
            print(i)
            self.vehicle.simple_goto(i)
            while not self.__is_i(i):
                time.sleep(1)
                input_gol.set_fei_ji_jiao(self.vehicle.attitude.yaw)
                if input_gol.information_position_is_empty():
                    continue
                destination = photo()
                location = i
                self.go_and_back(destination)
                self.vehicle.simple_goto(location)
        # 等待实时识别线程结束
        recognition_thread.join()

    # 这条语句将创建一个位于南纬35.361354，东经149.165218，相对home点高20m的位置
    def read_location(self):
        self.LocationGlobalRelativeList = [
            LocationGlobalRelative(36.22222, 117.03250, 12),
            LocationGlobalRelative(36.22278, 117.03250, 12),
            LocationGlobalRelative(36.22194, 117.03083, 12),
            LocationGlobalRelative(36.22167, 117.03167, 12),
            LocationGlobalRelative(36.22222, 117.03250, 12),
            #LocationGlobalRelative(-35.36349225, 149.16507274, 12),
        ]

    def arm_and_takeoff(self, aTargetAltitude):
        # 进行起飞前检查
        print("Basic pre-arm checks")
        # vehicle.is_armable会检查飞控是否启动完成、有无GPS fix、卡曼滤波器
        # 是否初始化完毕。若以上检查通过，则会返回True
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        # 解锁无人机（电机将开始旋转）
        print("Arming motors")
        # 将无人机的飞行模式切换成"GUIDED"（一般建议在GUIDED模式下控制无人机）
        self.vehicle.mode = VehicleMode("GUIDED")
        # 通过设置vehicle.armed状态变量为True，解锁无人机
        self.vehicle.armed = True

        # 在无人机起飞之前，确认电机已经解锁
        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        # 发送起飞指令
        print("Taking off!")
        # simple_takeoff将发送指令，使无人机起飞并上升到目标高度
        self.vehicle.simple_takeoff(aTargetAltitude)

        # 在无人机上升到目标高度之前，阻塞程序
        while True:
            print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
            # 当高度上升到目标高度的0.95倍时，即认为达到了目标高度，退出循环
            # vehicle.location.global_relative_frame.alt为相对于home点的高度
            if self.vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Reached target altitude")
                break
            # 等待1s
            time.sleep(1)

    # 飞过去操作，并且飞回来
    def go_and_back(self, destination: LocationGlobalRelative):
        print("go")
        local = self.vehicle.location.global_relative_frame
        self.vehicle.simple_goto(destination)
        while not self.__is_i(destination):
            time.sleep(1)

        print("back")
        # 飞回来
        self.vehicle.simple_goto(local)
        while not self.__is_i(local):
            time.sleep(1)

    def real_time_recognition(self):
        # 从起飞到降落一直进行识别
        while self.vehicle.mode.name != "LAND":
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                continue

            location = self.vehicle.location.global_relative_frame
            height = location.alt
            photo_again_operation(frame, height, location)

            cv.imshow('Drone Camera Stream', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    input_gol._init()
    fei = fei_ji()
    try:
        fei.start()
    except KeyboardInterrupt:
        del fei
    else:
        del fei

'''
飞往目的地：无人机飞往 destination 参数指定的位置。
到达检查：通过 while not self.__is_i(destination): 循环，无人机会持续检查是否已经到达目的地。一旦到达，循环结束。
拍照操作：到达目的地后，调用 photo_again_operation() 函数来执行拍照操作。这个函数在 Photo 模块中定义，但具体的拍照逻辑在提供的代码中是一个空函数，这意味着实际的拍照逻辑需要在该函数中实现。
返回起始点：拍照完成后，无人机将飞回起始位置。
这个过程在 fei_ji 类的 start 方法中被循环执行，针对 self.LocationGlobalRelativeList 列表中的每个位置坐标。
'''