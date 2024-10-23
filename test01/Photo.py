import threading

from dronekit import LocationGlobalRelative
import queue
import input_gol


def photo() -> LocationGlobalRelative:
    print("photo")
    return input_gol.get_information_position()


def jiao_juli_information_put_int_que(jiao: float, juli: float) -> None:
    if jiao == 0 and juli == 0:
        input_gol.put_information_position(None)
    fei_ji_jiao = input_gol.get_fei_ji_jiao()
    input_gol.put_information_position(LocationGlobalRelative(0, 0, 2))


def photo_again_operation():
    pass


def thread_for_shi_pin(high: float):
    def func():
        while True:
            readlist = [float(i) for i in input().split()]
            input_gol.put_information_position(LocationGlobalRelative(readlist[0], readlist[1], readlist[2]))

    threading.Thread(target=func, args=()).start()




if __name__ == "__main__":
    thread_for_shi_pin(10)
