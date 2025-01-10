from dronekit import connect
import sys

# 连接到无人机（在本例中为UDP端点）
try:
    vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=921600)
    # vehicle是Vehicle类的实例
except Exception as e:
    print("连接失败: ", e)
    sys.exit(1)

# 打印Autopilot Firmware版本
print("Autopilot Firmware version: %s" % vehicle.version)

# 打印Autopilot capabilities (supports ftp)
print("Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp)

# 打印Global Location
print("Global Location: %s" % vehicle.location.global_frame)

# 打印Global Location (relative altitude)
print("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)

# 打印Local Location
print("Local Location: %s" % vehicle.location.local_frame)  # NED

# 打印Attitude
print("Attitude: %s" % vehicle.attitude)

# 打印Velocity
print("Velocity: %s" % vehicle.velocity)

# 打印GPS
print("GPS: %s" % vehicle.gps_0)

# 打印Groundspeed
print("Groundspeed: %s" % vehicle.groundspeed)

# 打印Airspeed
print("Airspeed: %s" % vehicle.airspeed)

# 打印Gimbal status
print("Gimbal status: %s" % vehicle.gimbal)

# 打印Battery
print("Battery: %s" % vehicle.battery)

# 打印EKF OK?
print("EKF OK?: %s" % vehicle.ekf_ok)

# 打印Last Heartbeat
print("Last Heartbeat: %s" % vehicle.last_heartbeat)

# 打印Rangefinder
print("Rangefinder: %s" % vehicle.rangefinder)

# 打印Rangefinder distance
print("Rangefinder distance: %s" % vehicle.rangefinder.distance)

# 打印Rangefinder voltage
print("Rangefinder voltage: %s" % vehicle.rangefinder.voltage)

# 打印Heading
print("Heading: %s" % vehicle.heading)

# 打印Is Armable?
print("Is Armable?: %s" % vehicle.is_armable)

# 打印System status
print("System status: %s" % vehicle.system_status.state)

# 打印Mode
print("Mode: %s" % vehicle.mode.name)  # settable

# 打印Armed
print("Armed: %s" % vehicle.armed)  # settable