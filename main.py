#!/usr/bin/env python3
import visca
import tkinter
import time

cam = visca.Camera(device="/dev/ttyUSB0")

cam.set_zoom(0)
time.sleep(5)
print("direct: ", cam.get_status())

cam.set_pos(600, 65)
cam.set_zoom(1000)
time.sleep(5)
print("direct: ", cam.get_status())

cam.set_pos(400, 128)
cam.set_zoom(2800)
time.sleep(5)
print("reset: ", cam.get_status())

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

'''
print("reset: ", cam.get_status())
cam.zoom_in()
time.sleep(10)
print("zoom in: ", cam.get_status())
cam.zoom_out()
time.sleep(6)
print("zoom out: ", cam.get_status())

cam.move_down()
time.sleep(5)
print("down: ", cam.get_status())

cam.move_up()
time.sleep(5)
cam.set_zoom(1000)
time.sleep(5)
print("up: ", cam.get_status())

cam.move_left()
#cam.set_zoom(70)
time.sleep(5)
#cam.set_zoom(1900)
#time.sleep(5)
print("left: ", cam.get_status())

cam.move_right()
#time.sleep(5)
print("right: ", cam.get_status())

cam.set_pos(600, 65)
time.sleep(5)
print("direct: ", cam.get_status())

#cam.reset()
#cam.reset_camera()
cam.set_pos(400, 128)
time.sleep(2)
print("reset: ", cam.get_status())

time.sleep(2)

# print(cam.camid)
# print(cam.hwid)
# print(cam.swid)
'''