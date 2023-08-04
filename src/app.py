#!/usr/bin/env python3
#import time
from config import Config
from camera import Camera
from gui import Gui
import argparse

class Application:

    def __init__(self, fname, port):

        self.cfg = Config(fname)
        self.cam = Camera(device=port)
        self.gui = Gui(self.cfg, self.cam)

    def run(self):
        self.gui.run()

    def do_preset(self, name):
        self.cfg.go_preset(name, self.cam)
        #time.sleep(1)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="name of the configuration file to use", type=str)#, required=True)
    parser.add_argument("port", help="name of the serial port to use", type=str)#, required=True)
    args = parser.parse_args()

    Application(args.fname, args.port).run()
