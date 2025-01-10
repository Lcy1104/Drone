# main.py
import sys
import cv2 as cv
from dronekit import connect
from Photo import photo_again_operation  # 从photo.py导入photo_again_operation函数

# 连接到无人机
try:
    vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=921600)
except Exception as e:
    print("连接失败: ", e)
    sys.exit(1)

# 无人机摄像头处理
cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    location = vehicle.location.global_relative_frame
    height = location.alt

    photo_again_operation(frame, height, location)

    cv.imshow('Drone Camera Stream', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
