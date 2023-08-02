#!/usr/bin/env python3
import tkinter as tk
import time, os, sys
from camera import Camera
from config import Config

class Application:

    def __init__(self):

        self.cfg = Config('camera.cfg')
        self.cam = Camera(device=self.cfg.get_cam_port())

        self.app = tk.Tk()
        self.app.title("Camera Presets")
        self.app.geometry('350x450')

    def run(self):
        self.app.mainloop()

    def do_preset(self, name):
        self.cfg.go_preset(name, self.cam)
        time.sleep(1)

if __name__ == '__main__':

    app = Application()

    app.do_preset("default")
    app.do_preset("test 1")

    app.run()


