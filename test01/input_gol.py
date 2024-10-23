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
