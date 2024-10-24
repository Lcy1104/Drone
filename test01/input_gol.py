import queue
from dronekit import LocationGlobalRelative
def _init():
    global value
    global tui_chu_flag
    global fei_ji_jiao
    global information_position
    information_position = queue.Queue()
    value = True
    tui_chu_flag = False
    fei_ji_jiao = 0.0


def set_value(svalue: bool):
    global value
    value = svalue


def get_value() -> bool:
    return value


def set_tui_chu_flag(stui_chu_flag: bool):
    global tui_chu_flag
    tui_chu_flag = stui_chu_flag


def get_tui_chu_flag() -> bool:
    return tui_chu_flag


def set_fei_ji_jiao(sjiao: float):
    global fei_ji_jiao
    fei_ji_jiao = sjiao


def get_fei_ji_jiao() -> float:
    return fei_ji_jiao

def put_information_position(localR:LocationGlobalRelative):
    print("ya_ru")
    global information_position
    information_position.put(localR)


def get_information_position() -> LocationGlobalRelative:
    print("tan_chu")
    return information_position.get()

def information_position_is_empty() -> bool:
    global information_position
    return information_position.empty()

'''
_init函数：

初始化全局变量，包括一个队列information_position用于存储位置信息，一个布尔变量value用于控制某些操作，一个布尔变量tui_chu_flag可能用于标记输出状态，以及一个浮点变量fei_ji_jiao用于存储无人机的当前角度。
set_value和get_value函数：

这两个函数用于设置和获取value变量的值。
set_tui_chu_flag和get_tui_chu_flag函数：

这两个函数用于设置和获取tui_chu_flag变量的值。
set_fei_ji_jiao和get_fei_ji_jiao函数：

这两个函数用于设置和获取无人机的当前角度。
put_information_position和get_information_position函数：

put_information_position函数将一个LocationGlobalRelative对象放入队列中。
get_information_position函数从队列中取出一个LocationGlobalRelative对象。
information_position_is_empty函数：

这个函数检查队列是否为空，并返回一个布尔值。
'''