#!/usr/bin/env python3
#import time
from config import Config
from camera import Camera, NullCamera
from gui import Gui
import argparse
import sys

TEST_GUI = False

class Application:

    def __init__(self, fname):

        try:
            self.cfg = Config(fname)
            if not TEST_GUI:
                self.cam = Camera(device=self.cfg.get_port())
            else:
                self.cam = NullCamera(device=self.cfg.get_port())
            self.gui = Gui(self.cfg, self.cam)
        except Exception as e:
            sys.stderr(str(e))
            sys.exit(1)

    def run(self):
        self.gui.run()

    def do_preset(self, name):
        self.cfg.go_preset(name, self.cam)
        #time.sleep(1)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="name of the configuration file to use", type=str)#, required=True)
    args = parser.parse_args()

    Application(args.fname).run()
