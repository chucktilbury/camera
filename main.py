#!/usr/bin/env python3
import visca
import tkinter
import time

cam = visca.Camera()
# print("zoom position: ", hex(cam.get_zoom_pos()))
# print("focus position: ", hex(cam.get_focus_pos()))
# print("focus mode: ", cam.get_focus_mode())
# print("wb mode: ", cam.get_wb_mode())
# print("ae mode: ", cam.get_ae_mode())
#print("shutter pos: ", cam.get_shutter_pos())
#print("iris pos: ", cam.get_iris_pos())
#time.sleep(1)
#print("gain pos: ", cam.get_gain_pos())
#print("bright pos ", cam.get_bright_pos())

# cam.set_up_speed(5, 5)
# cam.set_stop_speed(5, 5)

print("reset: ", cam.get_pos())

#cam.reset()
cam.move_down(0x1f, 0x1f)
time.sleep(5)
print("down: ", cam.get_pos())

cam.move_up(0x1f, 0x1f)
time.sleep(5)
print("up: ", cam.get_pos())

cam.move_left(0x1f, 0x1f)
time.sleep(5)
print("left: ", cam.get_pos())

cam.move_right(0x1f, 0x1f)
time.sleep(5)
print("right: ", cam.get_pos())

cam.set_pos(0x1f, 0x1f, 600, 65)
time.sleep(5)
print("direct: ", cam.get_pos())


cam.reset()
time.sleep(2)
print("reset: ", cam.get_pos())

cam.close()

# print(cam.camid)
# print(cam.hwid)
# print(cam.swid)