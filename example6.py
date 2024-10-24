"""
Simple script for take off and control with arrow keys
"""


import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import Tkinter as tk


#
# connection_string = '10.42.0.1:14550'
print('Connecting...')
# vehicle = connect('10.42.0.1:14550',wait_ready=False,baud=921600)
vehicle = connect('/dev/ttyUSB0',wait_ready=False,baud=921600)
vehicle.wait_ready(True,raise_exception=False)

#
gnd_speed = 0.2 # [m/s]

#
def arm_and_takeoff(altitude):

   print("Arming motors")
   vehicle.mode = VehicleMode("GUIDED")
   vehicle.armed = True

   while not vehicle.armed: time.sleep(1)

   print("Taking Off")
   vehicle.simple_takeoff(altitude)

   while True:
      v_alt = vehicle.location.global_relative_frame.alt
      print(">> Altitude = %.1f m"%v_alt)
      if v_alt >= altitude * 0.95:
          print("Target altitude reached")
          break
      time.sleep(1)

#
def set_velocity_body(vehicle, vx, vy, vz):
    """ Remember: vz is positive downward!!!
    
    
    Bitmask to indicate which dimensions should be ignored by the vehicle 
    (a value of 0b0000000000000000 or 0b0000001000000000 indicates that 
    none of the setpoint dimensions should be ignored). Mapping: 
    bit 1: x,  bit 2: y,  bit 3: z, 
    bit 4: vx, bit 5: vy, bit 6: vz, 
    bit 7: ax, bit 8: ay, bit 9:
    
    
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()


#
def key(event):
    if event.char == event.keysym: #-- standard keys
        if event.keysym == 'r':
            print("r pressed >> Set the vehicle to RTL")
            vehicle.mode = VehicleMode("RTL")
        elif event.keysym == 'l':
            print("l pressed >> Set the vehicle to LAND")
            vehicle.mode = VehicleMode("LAND")

    else: #-- non standard keys
        if event.keysym == 'Up':
            set_velocity_body(vehicle, gnd_speed, 0, 0)
        elif event.keysym == 'Down':
            set_velocity_body(vehicle,-gnd_speed, 0, 0)
        elif event.keysym == 'Left':
            set_velocity_body(vehicle, 0, -gnd_speed, 0)
        elif event.keysym == 'Right':
            set_velocity_body(vehicle, 0, gnd_speed, 0)


#
#
arm_and_takeoff(0)

#
root = tk.Tk()
print(">> Control the drone with the arrow keys. Press r for RTL mode")
print(">> Control the drone with the arrow keys. Press l for LAND mode")
root.bind_all('<Key>', key)
root.mainloop()

'''
使用`dronekit`库来控制无人机，并使用`Tkinter`库创建一个图形用户界面（GUI），通过键盘的箭头键来控制无人机的移动。以下是代码的详细解释：

1. 导入所需的模块，包括`time`、`dronekit`和`Tkinter`。

3-4行：打印连接信息，并尝试通过串口`/dev/ttyUSB0`连接到无人机。这里使用的是本地连接，而不是无线连接。

6行：定义地面速度`gnd_speed`为0.2米/秒。

8-21行：定义`arm_and_takeoff`函数，用于武装无人机并使其起飞到指定高度。首先，它将无人机设置为GUIDED模式并武装电机。然后，它使用`simple_takeoff`命令使无人机起飞，并等待直到达到目标高度的95%。

23-37行：定义`set_velocity_body`函数，用于设置无人机在机体坐标系中的速度。这个函数发送一个MAVLink消息，告诉无人机以特定的速度在x、y、z方向上移动。注意，z方向的速度是向下为正。

39-53行：定义`key`函数，这是一个回调函数，用于处理键盘事件。当用户按下箭头键时，它会调用`set_velocity_body`函数来控制无人机的移动。如果用户按下'r'键，它会将无人机设置为返回到起飞点的模式（RTL）。如果按下'l'键，它会将无人机设置为降落模式（LAND）。

55行：调用`arm_and_takeoff`函数，使无人机起飞到0米的高度。这通常用于校准和准备控制。

57-65行：创建一个`Tkinter`窗口，并绑定键盘事件到`key`函数。这样，当用户在窗口中按下箭头键或'r'/'l'键时，`key`函数会被调用。然后，脚本进入主事件循环，等待用户的输入。

这个脚本允许用户通过GUI界面使用键盘的箭头键来控制无人机的前后左右移动，以及通过'r'和'l'键来控制无人机的返回和降落。这种方式适合于需要实时控制无人机的情况，例如在飞行模拟器中测试无人机的行为或者在实际飞行中进行简单的操作。在实际使用之前，需要确保无人机的固件和硬件设置正确，并且操作环境安全。

'''