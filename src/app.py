#!/usr/bin/env python3
#import time
from config import Config
from camera import Camera
from gui import Gui

class Application:

    def __init__(self):

        self.cfg = Config('camera.cfg')
        self.cam = Camera(device=self.cfg.get_port())
        self.gui = Gui(self.cfg, self.cam)

    def run(self):
        self.gui.run()

    def do_preset(self, name):
        self.cfg.go_preset(name, self.cam)
        #time.sleep(1)

if __name__ == '__main__':

    app = Application()

    #app.do_preset("Default")
    #app.do_preset("test")

    app.run()
