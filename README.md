# Serial Visca

Simple library to drive a single TTC8-0x camera over a serial port. This application implements a simple GUI to allow for camera presets. A preset is a Pan-Tilt-Zoom (PTZ) combination that can be arbitrarily switched by name using the GUI.

When a preset is added or modified, it is added to a pickle file that is native to Python. The data structure looks like this:

```{python}
pds = {
    "port": "string", # the serial port the camera is connected to
    "name": "string", # the name of the camera
    [{  # list of presets
        "name": "string",   # name of the preset
        "pan": number,      # pan value
        "tilt": number,     # tilt value
        "zoom": number,     # zoom value
        },
        ...
        {...}]
}
```

The GUI provides for PTZ buttons with speed controls that allows the camera to be aimed and the preset saved with the name. Then a list of presets is presented along with a "GO" button that allows a preset to be identified and selected easily at show time.

