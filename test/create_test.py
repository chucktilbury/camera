import pickle

DEFAULT_CFG_FILE='camera.cfg'
DEFAULT_CFG_NAME='Default Config'
DEFAULT_CFG_PORT='/dev/ttyUSB0'

data = {}
data['cam_name'] = DEFAULT_CFG_NAME
data['cam_port'] = DEFAULT_CFG_PORT

data['presets'] = {}

data['presets']['Default'] = {}
data['presets']['Default']['pan'] = 410
data['presets']['Default']['tilt'] = 220
data['presets']['Default']['zoom'] = 1000

data['presets']['test 1'] = {}
data['presets']['test 1']['pan'] = 510
data['presets']['test 1']['tilt'] = 120
data['presets']['test 1']['zoom'] = 1000

data['presets']['test 2'] = {}
data['presets']['test 2']['pan'] = 85
data['presets']['test 2']['tilt'] = 20
data['presets']['test 2']['zoom'] = 1500

data['presets']['test 3'] = {}
data['presets']['test 3']['pan'] = 700
data['presets']['test 3']['tilt'] = 400
data['presets']['test 3']['zoom'] = 0

data['presets']['test 4'] = {}
data['presets']['test 4']['pan'] = 400
data['presets']['test 4']['tilt'] = 20
data['presets']['test 4']['zoom'] = 2000

with open(DEFAULT_CFG_FILE, "wb") as fh:
    pickle.dump(data, fh)
