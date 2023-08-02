#!/usr/bin/env python3
import visca
import tkinter as tk
import time
from config import Config

pst = Config("test.pickle")
cam = visca.Camera(device=pst.get_cam_port())

pst.go_preset("test preset 1", cam)
time.sleep(5)
pst.go_preset("test preset 2", cam)
time.sleep(5)
pst.go_preset("test preset 3", cam)

app = tk.Tk()
app.title("Camera Presets")
app.geometry('350x400')
app.mainloop()

