import sys
import time

import cv2
from ultralytics import YOLO

# 添加YOLOv8目录到系统路径
yolov8_path = 'F:/Drone/yolov8/main'  # 替换为你的YOLOv8目录的实际路径
sys.path.append(yolov8_path)

# 加载模型
# 替换为您的模型文件路径
model_path = 'F:/Drone/yolov8/yolov8m-seg.pt'
model = YOLO(model_path)

# 检查输入类型
input_type = 'video'  # 或者 'video' 如果你想使用本地视频文件
input_source = 'E:/system/video/bilibili/978117942/output.mp4'  # 摄像头ID0，对于本地视频文件，这是视频文件的路径

if input_type == 'video':
    cap = cv2.VideoCapture(input_source)  # 使用视频文件路径
else:
    cap = cv2.VideoCapture(input_source)  # 使用摄像头ID

# 获取视频流的FPS（每秒帧数）
fps = cap.get(cv2.CAP_PROP_FPS)

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法接收帧（流结束？）。退出中...")
        break

    # 将帧转换为模型需要的格式
    results = model(frame)

    # 绘制检测结果
    annotated_frame = results[0].plot()

    # 显示图像
    cv2.imshow('YOLOv8 Detection', annotated_frame)

    # 按'q'退出
    if cv2.waitKey(1) == ord('q'):
        break

    # 尝试与视频流的FPS同步
    time.sleep(1 / fps)

# 释放资源
cap.release()
cv2.destroyAllWindows()