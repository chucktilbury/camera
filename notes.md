# Random notes

* Bug: when a preset is added or deleted, the camera is not updated, but the listed preset in the combobox changes. This can lead to confusion. Need to find a better way.
* There is no way to change the name of the config file.
* Need to have absolute config file and the port name as mandatory command parameters.
* Reset button?
* Reboot button?
* Drop down menu?
* BUG: If the camera class can't open the serial port then raise an exception and exit there instead of continuing.

* get the port from the config file instead of the command line.
* do not load the default preset into the camera upon start, but read the state of the camera after the reset.