from __future__ import print_function

import math
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from Photo import photo, photo_again_operation, thread_for_shi_pin
from pymavlink import mavutil
# from s2022_10_29_for_debug import thread_for_shi_pin
import input_gol


# -------------------------------------------------------------------------------------------------------
class fei_ji():
    def __init__(self):
        connection_string = '10.42.0.10:14550'
        print('Connecting to vehicle on: %s' % connection_string)
        self.vehicle = connect(connection_string, wait_ready=True, baud=921600)
        # 起飞
        self.arm_and_takeoff(10)

        print("Set default/target airspeed to 3")
        self.vehicle.airspeed = 7

        self.info = False
        self.dst = 10
        self.jiao = 60
        self.si_xun_huan = 0
        self.LocationGlobalRelativeList = []
        self.read_location()

    def __del__(self):
        # 发送"返航"指令
        print("Returning to Launch")
        # 返航，只需将无人机的飞行模式切换成"RTL(Return to Launch)"
        # 无人机会自动返回home点的正上方，之后自动降落
        self.vehicle.mode = VehicleMode("RTL")
        # 退出之前，清除vehicle对象
        print("Close vehicle object")
        self.vehicle.close()

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

    def read_location(self):
        self.LocationGlobalRelativeList = [
            LocationGlobalRelative(-35.36349225, 149.16507274, 10),
            LocationGlobalRelative(-35.36259419, 149.16507711, 10),
            LocationGlobalRelative(-35.36260491, 149.16617833, 10),
            LocationGlobalRelative(-35.36348865, 149.16618275, 10),
            LocationGlobalRelative(-35.36349225, 149.16507274, 10),
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

        # 拍照操作
        photo_again_operation()

        print("back")
        # 飞回来
        self.vehicle.simple_goto(local)
        while not self.__is_i(local):
            time.sleep(1)


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