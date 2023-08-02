#!/usr/bin/env python3
from camera import Camera
import tkinter as tk
import time
from config import Config
import os, sys

pst = Config('camera.cfg')
cam = Camera(device=pst.get_cam_port())
pst.go_preset("default", cam)

pst.go_preset("test 1", cam)
#time.sleep(5)
#pst.go_preset("test preset 2", cam)
#time.sleep(5)
#pst.go_preset("test preset 3", cam)

app = tk.Tk()
app.title("Camera Presets")
app.geometry('350x450')
app.mainloop()

