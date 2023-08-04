#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tktooltip import ToolTip
import time
from config import Config
from pprint import pprint as pp

MAX_PAN=800
MAX_TILT=400
MAX_ZOOM=2885

class NewDialog(tk.Toplevel):

    def __init__(self, master, *args):
        tk.Toplevel.__init__(self, master, *args)
        self.title('New Preset')
        #self.geometry('150x150')
        self.resizable(False, False)
        self.grab_set()

        self.app = master
        self.build_frame()
        self.wait_window()


    def build_frame(self):

        frame = ttk.Frame(self)
        frame.grid(row=0, column=0)#, padx=25, pady=25)

        wid = tk.Label(frame, text='Enter the name of new preset')
        wid.grid(row=0, column=0, padx=5, pady=5)

        self.name  = tk.StringVar()
        wid = tk.Entry(frame)
        wid['textvariable'] = self.name
        wid.grid(row=1, column=0, padx=5, pady=5)
        ToolTip(wid, msg='Name to save the preset under', delay=0.25)


        status = ttk.Frame(frame)
        status.grid(row=2, column=0, padx=5, pady=5)

        self.data = self.app.get_status()
        b1 = ttk.Frame(status)
        b1['padding'] = (15,0)
        b1.grid(row=0, column=0, sticky=tk.EW)
        wid = tk.Label(b1, text="Pan:")
        wid.grid(row=0, column=0, sticky=tk.E, padx=0, pady=0)
        self.pan_status = tk.Label(b1)
        self.pan_status['text'] = self.data['pan']
        self.pan_status.grid(row=0, column=1, sticky=tk.W, padx=0, pady=0)

        b2 = ttk.Frame(status)
        b2['padding'] = (15,0)
        b2.grid(row=0, column=1, sticky=tk.EW)
        wid = tk.Label(b2, text="Tilt:")
        wid.grid(row=0, column=0, sticky=tk.E, padx=0, pady=0)
        self.tilt_status = tk.Label(b2)
        self.tilt_status['text'] = self.data['tilt']
        self.tilt_status.grid(row=0, column=1, sticky=tk.W, padx=0, pady=0)

        b3 = ttk.Frame(status)
        b3['padding'] = (15,0)
        b3.grid(row=0, column=2, sticky=tk.EW)
        wid = tk.Label(b3, text="Zoom:")
        wid.grid(row=0, column=0, sticky=tk.E, padx=0, pady=0)
        self.zoom_status = tk.Label(b3)
        self.zoom_status['text'] = self.data['zoom']
        self.zoom_status.grid(row=0, column=1, sticky=tk.W, padx=0, pady=0)

        b4 = ttk.Frame(frame)
        b4['padding'] = (50,0)
        b4.grid(row=3, column=0, sticky=tk.EW)

        wid = tk.Button(b4, text = "Save", command=self.save_button)
        wid.grid(row=0, column=0, padx=5, pady=5)

        wid = tk.Button(b4, text = "Cancel", command=self.destroy)
        wid.grid(row=0, column=1, padx=5, pady=5)

    def save_button(self):

        name = self.name.get().strip()
        if len(name) == 0:
            messagebox.showerror('Error', 'Name cannot be blank')
            return

        if name in self.app.cfg.data['presets']:
            messagebox.showerror('Error', 'Name is not unique')
            return

        self.app.cfg.make_preset(name, self.data['pan'], self.data['tilt'], self.data['zoom'])
        self.app.cfg.save()
        self.app.cfg.load()
        pp(self.app.cfg.data)

        self.destroy()

class Gui(tk.Tk):

    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.title("Camera Presets")
        #self.geometry('360x550')
        self.resizable(False, False)

        # supporting monkey patching the callbacks. Re-assign these to connect
        # them up to the other stuff.
        self.up_callback = self.up_button
        self.down_callback = self.down_button
        self.left_callback = self.left_button
        self.right_callback = self.right_button
        self.zoom_in_callback = self.in_button
        self.zoom_out_callback = self.out_button
        self.new_callback = self.new_button
        self.save_callback = self.save_button
        self.del_callback = self.del_button
        self.preset_callback = self.preset_ctl
        self.internal_status = {'pan':0, 'tilt':0, 'zoom':0}

        self.preset_name = 'Default'
        self.main_layout()
        self.update_status()

    def run(self):
        '''
        Run the GUI state machine.
        '''
        self.mainloop()

    def main_layout(self):
        '''
        Main window with the internal frames.
        '''
        # frame for whole window
        frame = ttk.Frame(self)
        frame['borderwidth'] = 2
        frame['relief'] = 'sunken'
        frame.grid_columnconfigure(0,weight=1)
        frame.grid(row=0, column=0, sticky=tk.EW)

        # frames for the window sections
        # top frame contains data that applies to all presets
        top_frame = self.make_top_frame(frame)
        top_frame['borderwidth'] = 2
        top_frame['relief'] = 'sunken'
        top_frame['padding'] = (30,5)
        top_frame.grid(row=0, column=0, sticky=tk.EW)

        # center frame contains the movement buttons and other controls
        center_frame = self.make_center_frame(frame)
        center_frame['borderwidth'] = 2
        center_frame['relief'] = 'sunken'
        center_frame['padding'] = (5,5)
        center_frame.grid(row=1, column=0, sticky=tk.EW)

        # bottom frame contains controls such as save and quit
        bottom_frame = self.make_bottom_frame(frame)
        bottom_frame['borderwidth'] = 2
        bottom_frame['relief'] = 'sunken'
        bottom_frame['padding'] = (25,5)
        bottom_frame.grid(row=2, column=0, sticky=tk.EW)

        self.get_status()


    def make_top_frame(self, parent):
        '''
        Top frame of the main window.
        '''
        frame = ttk.Frame(parent)

        wid = tk.Label(frame, text="Camera Name:")
        wid.grid(row=0,column=0, sticky=tk.E, padx=5, pady=5)

        self.cam_name = ttk.Label(frame)
        self.cam_name['text'] = self.cfg.get_name()
        self.cam_name.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        wid = tk.Label(frame, text="Port Name:")
        wid.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)

        self.cam_port = ttk.Label(frame)
        self.cam_port['text'] = self.cfg.get_port()
        self.cam_port.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        wid = tk.Label(frame, text="Select Preset:")
        wid.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)

        self.preset_list = []
        for s in self.cfg.data['presets']:
            self.preset_list.append(s)

        #self.crnt_preset = tk.StringVar(frame)
        # self.crnt_preset.set(self.preset_list[0])
        self.opt_ctl = ttk.Combobox(frame, values=self.preset_list)
        self.opt_ctl.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.opt_ctl.set(self.preset_list[0])
        self.opt_ctl.bind('<<ComboboxSelected>>', self.preset_ctl)
        self.opt_ctl['state'] = 'readonly'
        # self.crnt_preset.trace('w', self.preset_ctl)
        ToolTip(self.opt_ctl, msg='Select the preset and go to it.', delay=0.25)

        return frame

    def make_center_frame(self, parent):
        '''
        Middle frame of the main window.
        '''
        frame = ttk.Frame(parent)

        #
        # PAN/TILT BUTTONS
        #
        top = ttk.Frame(frame)
        top['borderwidth'] = 2
        top['relief'] = 'sunken'
        top['padding'] = (20,0)
        top.grid(row=0, column=0, sticky=tk.EW)

        wid = tk.Label(top, text="Pan/Tilt")
        wid.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        t1 = ttk.Frame(top)
        t1['padding'] = (20,0)
        t1.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        wid = tk.Button(t1, text="up", command=self.up_callback)
        wid.grid(row=0, column=1, sticky=tk.EW)
        ToolTip(wid, delay=0.25, msg='Move the camera UP')
        wid = ttk.Button(t1, text="left", command=self.left_callback)
        ToolTip(wid, delay=0.25, msg='Move the camera LEFT')
        wid.grid(row=1, column=0, sticky=tk.EW)
        wid = ttk.Button(t1, text="right", command=self.right_callback)
        ToolTip(wid, delay=0.25, msg='Move the camera RIGHT')
        wid.grid(row=1, column=2, sticky=tk.EW)
        wid = ttk.Button(t1, text="down", command=self.down_callback)
        ToolTip(wid, delay=0.25, msg='Move the camera DOWN')
        wid.grid(row=2, column=1, sticky=tk.EW)

        #
        # ZOOM BUTTONS
        #
        wid = tk.Label(top, text="Zoom")
        wid.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        t2 = ttk.Frame(top)
        t2['padding'] = (65,0)
        t2.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

        wid = ttk.Button(t2, text="in", command=self.zoom_in_callback)
        wid.grid(row=0, column=0, sticky=tk.EW)
        ToolTip(wid, delay=0.25, msg='Zoom the camera closer')
        wid = ttk.Button(t2, text="out", command=self.zoom_out_callback)
        wid.grid(row=0, column=1, sticky=tk.EW)
        ToolTip(wid, delay=0.25, msg='Zoom the camera further away')

        #
        # PAN/TILT SLIDER
        #
        center = ttk.Frame(frame)
        center['borderwidth'] = 2
        center['relief'] = 'sunken'
        center['padding'] = (5,0)
        center.grid(row=1, column=0, sticky=tk.EW)

        wid = tk.Label(center, text="Pan/Tilt:")
        wid.grid(row=0,column=0, sticky=tk.SE, padx=5, pady=5)

        self.movement_increment = tk.IntVar()
        wid = tk.Scale(center)
        wid['orient']=tk.HORIZONTAL
        wid['variable']=self.movement_increment
        wid['from_']=1
        wid['to']=10
        wid['length']=240
        ToolTip(wid, delay=0.25, msg='Set the camera increment for moving.')
        self.movement_increment.set(5)
        wid.grid(row=0,column=1, sticky=tk.E, padx=5, pady=5)

        #
        # ZOOM SLIDER
        #
        wid = tk.Label(center, text="Zoom:")
        wid.grid(row=1, column=0, sticky=tk.SE, padx=5, pady=5)

        self.zoom_increment = tk.IntVar()
        wid = tk.Scale(center)
        wid['orient']=tk.HORIZONTAL
        wid['variable']=self.zoom_increment
        wid['from_']=10
        wid['to']=100
        wid['length']=240
        ToolTip(wid, delay=0.25, msg='Set the camera increment for zoom.')
        self.zoom_increment.set(50)
        wid.grid(row=1,column=1, sticky=tk.E, padx=5, pady=5)

        #
        # STATUS DISPLAY
        #
        bottom = ttk.Frame(frame)
        bottom['borderwidth'] = 2
        bottom['relief'] = 'sunken'
        bottom['padding'] = (20,0)
        bottom.grid(row=2, column=0, sticky=tk.EW)

        wid = tk.Label(bottom, text="Status")
        wid.grid(row=0, column=1, sticky=tk.EW, padx=20, pady=5)

        stat = self.cfg.get_preset(self.opt_ctl.get())

        b1 = ttk.Frame(bottom)
        b1['padding'] = (15,0)
        b1.grid(row=1, column=0, sticky=tk.EW)
        wid = tk.Label(b1, text="Pan:")
        wid.grid(row=0, column=0, sticky=tk.E, padx=0, pady=0)
        self.pan_status = tk.Label(b1)
        self.pan_status['text'] = stat['pan']
        self.pan_status.grid(row=0, column=1, sticky=tk.W, padx=0, pady=0)

        b2 = ttk.Frame(bottom)
        b2['padding'] = (15,0)
        b2.grid(row=1, column=1, sticky=tk.EW)
        wid = tk.Label(b2, text="Tilt:")
        wid.grid(row=0, column=0, sticky=tk.E, padx=0, pady=0)
        self.tilt_status = tk.Label(b2)
        self.tilt_status['text'] = stat['tilt']
        self.tilt_status.grid(row=0, column=1, sticky=tk.W, padx=0, pady=0)

        b3 = ttk.Frame(bottom)
        b3['padding'] = (15,0)
        b3.grid(row=1, column=2, sticky=tk.EW)
        wid = tk.Label(b3, text="Zoom:")
        wid.grid(row=0, column=0, sticky=tk.E, padx=0, pady=0)
        self.zoom_status = tk.Label(b3)
        self.zoom_status['text'] = stat['zoom']
        self.zoom_status.grid(row=0, column=1, sticky=tk.W, padx=0, pady=0)

        return frame

    def make_bottom_frame(self, parent):
        '''
        Bottom frame of the main window.
        '''
        frame = ttk.Frame(parent)

        padx = 10
        wid = tk.Button(frame, text='New', command=self.new_callback)
        ToolTip(wid, delay=0.25, msg='Create a new preset from the current\nstate with a new name.')
        wid.grid(row=0, column=0, padx=padx, pady=0)

        wid = tk.Button(frame, text='Delete', command=self.del_callback)
        ToolTip(wid, delay=0.25, msg='Delete the current preset.')
        wid.grid(row=0, column=1, padx=padx, pady=0)

        wid = tk.Button(frame, text='Save', command=self.save_callback)
        ToolTip(wid, delay=0.25, msg='Save the current state of the camera into the\ncurrent preset name.')
        wid.grid(row=0, column=2, padx=padx, pady=0)

        wid = tk.Button(frame, text='Quit', command=self.quit_button)
        ToolTip(wid, delay=0.25, msg='End the camera program.')
        wid.grid(row=0, column=3, padx=padx, pady=0)

        return frame

    def update_status(self):
        '''
        Update the GUI in response to a completed action.
        '''
        self.preset_name = self.opt_ctl.get()
        #self.internal_status = self.cfg.get_preset(self.preset_name)
        print("update",)
        self.pan_status['text'] = str(self.internal_status['pan'])
        self.tilt_status['text'] = str(self.internal_status['tilt'])
        self.zoom_status['text'] = str(self.internal_status['zoom'])
        pp(self.internal_status)
        self.cam_name['text'] = self.cfg.get_name()
        self.cam_port['text'] = self.cfg.get_port()

    def get_status(self):
        '''
        Return the internal status of the GUI as a result of a request from a user.
        '''
        self.preset_name = self.opt_ctl.get()
        self.internal_status['pan'] = int(self.pan_status['text'])
        self.internal_status['tilt'] = int(self.tilt_status['text'])
        self.internal_status['zoom'] = int(self.zoom_status['text'])
        print("get status",)
        pp(self.internal_status)

        return {'name': self.preset_name,
                'pan': self.internal_status['pan'],
                'tilt': self.internal_status['tilt'],
                'zoom': self.internal_status['zoom']}

    def preset_ctl(self, var1): #, var2, var3):
        self.preset_name = self.opt_ctl.get()
        self.internal_status = self.cfg.get_preset(self.preset_name)
        self.update_status()
        self.get_status()

    def new_button(self):
        NewDialog(self)
        print('<<here>>')
        self.preset_list = []
        for s in self.cfg.data['presets']:
            self.preset_list.append(s)
        self.opt_ctl['values'] = self.preset_list
        self.opt_ctl.set(self.preset_list[0])

    def del_button(self):
        self.get_status()
        r = messagebox.askyesno('Delete', 'Delete the preset named "'+self.preset_name+'"')
        if r:
            del self.cfg.data['presets'][self.preset_name]
            self.cfg.save()
            self.cfg.load()
            self.preset_list = []
            for s in self.cfg.data['presets']:
                self.preset_list.append(s)
            self.opt_ctl['values'] = self.preset_list
            self.opt_ctl.set(self.preset_list[0])

    def save_button(self):
        self.get_status()
        r = messagebox.askyesno('Save', 'Save the preset named "'+self.preset_name+'"')
        if r:
            self.cfg.save()

    def up_button(self):
        self.internal_status['tilt'] = self.internal_status['tilt'] - int(self.movement_increment.get())
        if self.internal_status['tilt'] < 0:
            self.internal_status['tilt'] = 0
        self.update_status()
        print("up")

    def down_button(self):
        self.internal_status['tilt'] = self.internal_status['tilt'] + int(self.movement_increment.get())
        if self.internal_status['tilt'] > MAX_TILT:
            self.internal_status['tilt'] = MAX_TILT
        self.update_status()
        print("down")

    def left_button(self):
        self.internal_status['pan'] = self.internal_status['pan'] - int(self.movement_increment.get())
        if self.internal_status['pan'] < 0:
            self.internal_status['pan'] = 0
        self.update_status()
        print("left")

    def right_button(self):
        self.internal_status['pan'] = self.internal_status['pan'] + int(self.movement_increment.get())
        if self.internal_status['pan'] > MAX_PAN:
            self.internal_status['pan'] = MAX_PAN
        self.update_status()
        print("right")

    def in_button(self):
        self.internal_status['zoom'] = self.internal_status['zoom'] + int(self.zoom_increment.get())
        if self.internal_status['zoom'] > MAX_ZOOM:
            self.internal_status['zoom'] = MAX_ZOOM
        self.update_status()
        print('in')

    def out_button(self):
        self.internal_status['zoom'] = self.internal_status['zoom'] - int(self.zoom_increment.get())
        if self.internal_status['zoom'] < 0:
            self.internal_status['zoom'] = 0
        self.update_status()
        print('out')

    def quit_button(self):
        self.destroy()

class Application:

    def __init__(self):

        self.cfg = Config('camera.cfg')
        #self.cam = Camera(device=self.cfg.get_cam_port())

        self.gui = Gui(self.cfg)

    def run(self):
        self.gui.run()

    def do_preset(self, name):
        self.cfg.go_preset(name, self.cam)
        time.sleep(1)

if __name__ == '__main__':

    app = Application()

    #app.do_preset("default")
    #app.do_preset("test 1")

    app.run()
