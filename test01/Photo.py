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