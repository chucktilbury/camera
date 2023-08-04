# Serial Visca

Simple library to drive a single TTC8-0x camera over a serial port. This
application implements a simple GUI to allow for camera presets. A preset is a
Pan-Tilt-Zoom (PTZ) combination that can be arbitrarily switched by name using
the GUI.

When a preset is added or modified, it is added to a pickle file that is native
to Python. The data structure looks like this:

```{python}
preset_data_structure = {
    "port": "string", # the serial port the camera is connected to
    "name": "string", # the name of the camera
    "presets": {    # dictionary of presets
        "name": {   # the preset name as the index
            "pan": number,  # pan value
            "tilt": number, # tilt value
            "zoom": number, # zoom value
        },
        ...
        "name": {
            ...
        }
    }
}
```

The GUI provides for PTZ buttons with speed controls that allows the camera to
be aimed and the preset saved with the name. Then a list of presets is presented
along with a "GO" button that allows a preset to be identified and selected
easily at show time.

## Development
To develop on this software, a working Python3.X interpreter is required and
pip must be installed and working. Other packages are virtualenv, tkinter,
pyserial, tkinter-tooltip. The pyinstall package is not required, but could
be nice to have.

There are several scripts provided to aid manipulating the virtual environment.
In general, if they are not being used in the correct context, they should
produce an error and refuse to run.

* Begin a new development session: ```bin/begin```. This creates an active
session and downloads any files that are missing from your development
environment.
* End the current development session: ```exit```.
* Clean a session and delete all generated files: ```clean```. Note that
this must be done in an active session.
* Build a stand-alone executable file in an active session: ```make``` or
```build```. Note that if you have trouble running a built application, then
be sure that all of the packages are installed in the system copy of python
and not just in the virtual environment. You can do that by running the command
```pip install -r requirements.txt``` while **not** in the build environment.
* Run the current version without building" ```python src/app.py camera.cfg /dev/ttyUSB0```
or ```camera camera.cfg /dev/ttyUSB0```

## Use
This assumes that you have already created a working serial cable to connect to
a Cisco or compatible with TTC8-02 camera. There is a user guide in the docs
directory of this repository. This also assumes that you know how to wire things
up and that you have it working. This software should work on any operating
system on which Python3, tkinter, and pyserial are supported. If a binary
application is to be distributed, then all of the DLL or SO files should be
included in the application directory.

### Configuration file
This application uses a configuration file to store the presets into. That file
can be located in one of several locations. It is searched for in this order.
* Check if the file can be opened as an absolute path
* Check in the current directory
* Walk all of the subdirectories from the current directory
* Check the directory where the executable is located
* Walk all of the subdirectories from the previous directory where the executable
is located.
If a file matching the name given on the command line is found, then we try to
load it as a configuration file. If an error happens then either the file could
not be found or it is not a valid configuration file.

#### Create a new configuration file
From a valid development environment, a new configuration file can be generated
as ```python test/create_cfg.py "Camera Name"```. This will create a file called
camera.cfg in the current directory. If you don't supply a camera name, then the
default name of "Default Config" is used. You can then move or copy this file to
any location you choose where the app can find it. Modify it using the application
to meet your needs. The contents of this configuration file should be close to
the reset values of the camera.

### Start the program
To start the program from the github repository directory, use the command
```python src/app.py camera.cfg /dev/ttyUSB0```. Substitute the configuration
name and the device name according to your needs and operating system.

There is a small program that becomes available in the development system called
pyserial-ports that gives a list of the available serial ports. This application
was developed and tested using a Belkin USB/Serial adapter.

