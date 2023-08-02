import pickle
from pprint import pprint as pp
import time, os


class Config:
    '''
    This class represents the state of the preset configuration file.
    '''

    def __init__(self, fname):
        self.fname = fname
        self.data = {}
        self.data['presets'] = {}

        # make sure file exists....
        if os.path.exists(self.fname):
            self.load()
        else:
            self.save()
            self.load()

    def save(self):
        '''
        Save the state of the configuration to the file.
        '''
        with open(self.fname, "wb") as fh:
            pickle.dump(self.data, fh)

    def load(self):
        '''
        Read the state of the configuration from the file.
        '''
        with open(self.fname, "rb") as fh:
            self.data = pickle.load(fh)

    def go_preset(self, name, cam):
        '''
        Control the camera to the PTZ setting.
        '''
        pset = self.get_preset(name)
        cam.set_pos(pset['pan'], pset['tilt'])
        cam.set_zoom(pset['zoom'])
        time.sleep(1)

    def set_cam_name(self, name):
        '''
        Set the camera name
        '''
        self.data['cam_name'] = name

    def get_cam_name(self):
        '''
        Get the camera name for display
        '''
        return self.data['cam_name']

    def set_cam_port(self, port):
        '''
        Set the camera serial port
        '''
        self.data['cam_port'] = port

    def get_cam_port(self):
        '''
        Set the camera serial port
        '''
        return self.data['cam_port']

    # in the future, this will read the settings from the camera
    def make_preset(self, name, pan, tilt, zoom):
        '''
        Create or update a preset in the data
        '''
        self.data['presets'][name] = {}
        self.data['presets'][name]['pan'] = pan
        self.data['presets'][name]['tilt'] = tilt
        self.data['presets'][name]['zoom'] = zoom

    def get_preset(self, name):
        '''
        Return the data for a specific preset
        '''
        return self.data['presets'][name]

    def show(self):
        pp(self.data)

