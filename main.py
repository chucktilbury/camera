#!/usr/bin/env python3
import visca
import tkinter

cam = visca.Camera()
cam.reset()
print(cam.get_camid())
cam.close()
