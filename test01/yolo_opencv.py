import cv2
import torch
import sys
import time

# 添加YOLOv5目录到系统路径
#yolov5_path = 'F:/Drone/yolo/5.0'  # 替换为你的YOLOv5目录的实际路径
yolov5_path = 'F:/Drone/yolo/5.0'
sys.path.append(yolov5_path)

# 加载模型
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

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
    results.render()

    # 获取绘制结果的图像
    det_frame = results.ims[0]

    # 显示图像
    cv2.imshow('YOLOv5 Detection', det_frame)

    # 按'q'退出
    if cv2.waitKey(1) == ord('q'):
        break

    # 尝试与视频流的FPS同步
    time.sleep(1 / fps)

# 释放资源
cap.release()
cv2.destroyAllWindows()
