import pickle
from pprint import pprint as pp
import os, sys

DEFAULT_CFG_FILE='camera.cfg'
DEFAULT_CFG_NAME='Default Config'
DEFAULT_CFG_PORT='/dev/ttyUSB0'

class ConfigError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Config Error: " + self.msg

class Config:
    '''
    This class represents the state of the preset configuration file.
    '''

    def __init__(self, fname=None):
        self.fname = self.find_config(fname)

        try:
            self.load()
        except Exception as e:
            raise ConfigError("Cannot load a configuration file")

    def create_default_config(self):
        '''
        Create a default configuration. It is not permissable for the camera
        app to begin without a valid configuration.
        '''
        # create the default config file in the same directory as the
        # executable.
        self.fname = os.path.join(
            os.path.abspath(
                os.path.dirname(sys.argv[0])), DEFAULT_CFG_FILE)

        self.data = {}
        self.data['cam_name'] = DEFAULT_CFG_NAME
        self.data['cam_port'] = DEFAULT_CFG_PORT
        self.data['presets'] = {}
        self.data['presets']['default'] = {}
        self.data['presets']['default']['pan'] = 400
        self.data['presets']['default']['tilt'] = 220
        self.data['presets']['default']['zoom'] = 0
        self.save()
        self.load()

    def find_config(self, name):
        '''
        Find a valid configuration file. If no valid file is found, then return
        None.
        '''
        if name is None:
            name = DEFAULT_CFG_FILE

        # check for an absolute path
        if os.path.isfile(name):
            return name

        # check in the current directory
        p = os.path.abspath('.')
        if os.path.isfile(os.path.join(p, name)):
            return os.path.join(p, name)

        # walk the current directory
        for root, dirs, files in os.walk(p):
            for s in dirs:
                pat = os.path.abspath(s)
                if os.path.isfile(os.path.join(pat, name)):
                    return os.path.join(pat, name)

        # check in the same directory as the executable
        p = os.path.abspath(os.path.dirname(sys.argv[0]))
        if os.path.isfile(os.path.join(p, name)):
            return os.path.join(p, name)

        # check in the previous dir from where the executable is located
        if os.path.isfile(os.path.join(p, name)):
            return os.path.join(p, name)

        # Walk the previous directory
        for root, dirs, files in os.walk(p):
            for s in dirs:
                pat = os.path.abspath(s)
                if os.path.isfile(os.path.join(pat, name)):
                    return os.path.join(pat, name)

        # could not be found
        raise ConfigError('Cannot find any config file')


    def save(self):
        '''
        Save the state of the configuration to the file.
        '''
        try:
            with open(self.fname, "wb") as fh:
                pickle.dump(self.data, fh)
        except FileNotFoundError as e:
            raise ConfigError("Cannot save configuration file: "+e)

    def load(self):
        '''
        Read the state of the configuration from the file.
        '''
        try:
            #print("loading:", self.fname)
            with open(self.fname, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError as e:
            raise ConfigError("Cannot load configuration file: "+e)
        except pickle.UnpicklingError as e:
            raise ConfigError("Invalid configuration file: "+str(e))

    def go_preset(self, name, cam):
        '''
        Control the camera to the PTZ setting.
        '''
        pset = self.get_preset(name)
        cam.set_pos(pset['pan'], pset['tilt'])
        cam.set_zoom(pset['zoom'])

    def set_name(self, name):
        '''
        Set the camera name
        '''
        self.data['cam_name'] = name

    def get_name(self):
        '''
        Get the camera name for display
        '''
        return self.data['cam_name']

    def set_port(self, port):
        '''
        Set the camera serial port
        '''
        self.data['cam_port'] = port

    def get_port(self):
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
        #print('get_preset:', name)
        #pp(self.data)
        return {'pan': self.data['presets'][name]['pan'],
                'tilt': self.data['presets'][name]['tilt'],
                'zoom': self.data['presets'][name]['zoom']}

    def show(self):
        pp(self.data)

