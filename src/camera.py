#!/usr/bin/env python3
import visca
import tkinter as tk
import time
from config import Config
import os, sys

'''
def search_dir(pat, name):

    if os.path.isfile(os.path.join(pat, name)):
        return os.path.join(pat, name)

    for root, dirs, files in os.walk(pat):
        for s in dirs:
            p = os.path.abspath(s)
            if os.path.isfile(os.path.join(p, name)):
                return os.path.join(p, name)

def find_config(name):

    if len(sys.argv) < 2:
        print("The config file is a required parameter.")
        sys.exit(1)

    # check for an absolute path
    if os.path.isfile(sys.argv[1]):
        return sys.argv[1]

    # check in the same directory as the executable
    p = os.path.abspath(os.path.dirname(sys.argv[0]))
    if os.path.isfile(os.path.join(p, sys.argv[1])):
        return os.path.join(p, sys.argv[1])

    # search the previous directory
    p = os.path.abspath(os.path.dirname(p))
    return search_dir(p, sys.argv[1])
'''

pst = Config('test.pickle')
cam = visca.Camera(device=pst.get_cam_port())
pst.go_preset("default", cam)

#pst.go_preset("test preset 1", cam)
#time.sleep(5)
#pst.go_preset("test preset 2", cam)
#time.sleep(5)
#pst.go_preset("test preset 3", cam)

app = tk.Tk()
app.title("Camera Presets")
app.geometry('350x400')
app.mainloop()

