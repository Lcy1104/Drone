import threading

from dronekit import LocationGlobalRelative
import queue
import input_gol
import os
import time
from datetime import datetime
import cv2 as cv
import numpy as np
import torch
from ultralytics import YOLO  # 导入YOLO类
import json


def photo() -> LocationGlobalRelative:
    print("photo")
    return input_gol.get_information_position()


def jiao_juli_information_put_int_que(jiao: float, juli: float) -> None:
    if jiao == 0 and juli == 0:
        input_gol.put_information_position(None)
    fei_ji_jiao = input_gol.get_fei_ji_jiao()
    input_gol.put_information_position(LocationGlobalRelative(0, 0, 2))


def photo_again_operation(image=None, height=None, location=None):
    # YOLO模型配置
    YOLO_CONFIG = {
        'classes': [
            "Ambulance", "Buffalo", "Bus", "Camel", "Car", "Cat", "Cheetah", "Cow", "Deer", "Dog", "Elephant", "Goat",
            "Gorilla", "Hippo", "Horse", "Lion", "Monkeys", "Motorcycle", "Panda", "Rat", "Rhino", "Tiger", "Truck",
            "Wolf",
            "Zebra", "ambulance", "army vehicle", "auto rickshaw", "bicycle", "bus", "car", "fire", "garbagevan",
            "human hauler",
            "minibus", "minivan", "motorbike", "person", "pickup", "policecar", "rickshaw", "scooter", "stagnant_water",
            "suv",
            "taxi", "three wheelers -CNG-", "truck", "van", "wheelbarrow"],  # 需要识别的目标类别
        'conf_threshold': 0.8,  # 置信度阈值
    }

    # 加载YOLO模型
    model = YOLO('/home/ubuntu/test/yolov8m.pt')  # 使用官方接口加载模型
    results = model(image)  # 进行YOLO目标检测

    # 检查是否有检测结果
    # 检查是否有检测结果
    if not results:
        print("No detections.")
        return

    # 创建根报告文件夹
    report_folder = 'report'
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    # 解析检测结果
    detection_results = []  # 用于存储所有检测结果的列表
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')  # 定义时间戳

    for result in results:
        boxes = result.boxes  # 使用boxes属性获取检测结果
        for i, box in enumerate(boxes.xyxy):
            conf = boxes.conf[i]
            cls = boxes.cls[i]
            if conf > YOLO_CONFIG['conf_threshold'] and model.names[int(cls)] in YOLO_CONFIG['classes']:
                category = model.names[int(cls)]
                x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])

                # 保存标记了位置的照片
                output_image_path = os.path.join(report_folder, f"{category}-{timestamp}.jpg")
                annotated_image = result.plot()  # 使用plot方法渲染检测框
                cv.imwrite(output_image_path, annotated_image)

                # 保存包含坐标和高度的json文件
                info_path = os.path.join(report_folder, f"{category}-{timestamp}.json")
                detection_result = {
                    "latitude": location.lat,
                    "longitude": location.lon,
                    "height": height,
                    "class": category,
                    "timestamp": timestamp,
                    "coordinates": (x1, y1, x2, y2)
                }
                detection_results.append(detection_result)

                # 将检测到的类别和照片路径写入json文件
                with open(info_path, 'w') as f:
                    json.dump(detection_result, f, indent=4)

    # 如果检测到特定类型，保存所有检测结果到json文件
    if detection_results:
        with open(os.path.join(report_folder, f"detections-{timestamp}.json"), 'w') as f:
            json.dump(detection_results, f, indent=4)


def thread_for_shi_pin(high: float):
    def func():
        while True:
            readlist = [float(i) for i in input().split()]
            input_gol.put_information_position(LocationGlobalRelative(readlist[0], readlist[1], readlist[2]))

    threading.Thread(target=func, args=()).start()


if __name__ == "__main__":
    thread_for_shi_pin(10)

'''
photo函数：

这个函数模拟了拍照操作，并返回一个LocationGlobalRelative对象，该对象包含了拍照时无人机的地理位置信息。这个位置信息是通过调用input_gol模块的get_information_position函数获取的。
jiao_juli_information_put_int_que函数：

这个函数接收两个参数：jiao（角度）和juli（距离）。如果这两个参数都为0，它会将None放入input_gol模块的队列中，表示没有有效的空间信息。否则，它会将一个包含无人机当前角度和固定高度（2米）的LocationGlobalRelative对象放入队列。
photo_again_operation函数：

这个函数目前是一个空函数，可能用于在未来的版本中实现重复拍照的操作。
thread_for_shi_pin函数：

这个函数启动一个新的线程，该线程不断从标准输入读取位置信息（经度、纬度、高度），并将这些信息作为LocationGlobalRelative对象放入input_gol模块的队列中。
'''
