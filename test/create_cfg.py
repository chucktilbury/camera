import pickle
import sys

DEFAULT_CFG_FILE='camera.cfg'
DEFAULT_CFG_NAME='Default Config'
DEFAULT_CFG_PORT='/dev/ttyUSB0'

MAX_PAN = 800
MIN_PAN = 0
MAX_TILT = 200
MIN_TILT = 0
MAX_ZOOM = 2880
MIN_ZOOM = 0
RESET_PAN = 410
RESET_TILT = 125
RESET_ZOOM = 0

if len(sys.argv) > 1:
    cam_name = sys.argv[1]
else:
    cam_name = DEFAULT_CFG_NAME

data = {}
data['cam_name'] = cam_name
#data['cam_port'] = DEFAULT_CFG_PORT

data['presets'] = {}

data['presets']['Default'] = {}
data['presets']['Default']['pan'] = RESET_PAN
data['presets']['Default']['tilt'] = RESET_TILT
data['presets']['Default']['zoom'] = RESET_ZOOM

# data['presets']['test 1'] = {}
# data['presets']['test 1']['pan'] = 510
# data['presets']['test 1']['tilt'] = 120
# data['presets']['test 1']['zoom'] = 1000

# data['presets']['test 2'] = {}
# data['presets']['test 2']['pan'] = 85
# data['presets']['test 2']['tilt'] = 20
# data['presets']['test 2']['zoom'] = 1500

# data['presets']['test 3'] = {}
# data['presets']['test 3']['pan'] = 700
# data['presets']['test 3']['tilt'] = 400
# data['presets']['test 3']['zoom'] = 0

# data['presets']['test 4'] = {}
# data['presets']['test 4']['pan'] = 400
# data['presets']['test 4']['tilt'] = 20
# data['presets']['test 4']['zoom'] = 2000

with open(DEFAULT_CFG_FILE, "wb") as fh:
    pickle.dump(data, fh)
