from dronekit import connect

# 连接到无人机（这里以UDP端点为例）
vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=921600)

# 打印飞控固件版本
print("Autopilot Firmware version: %s" % vehicle.version)