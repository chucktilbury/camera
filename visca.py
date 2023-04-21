#!/usr/bin/env python3
# https://coderslegacy.com/python/ctypes-tutorial/

import serial
import time

class Camera:
    '''
    Control functions for a single VISCA enabled camera over a
    serial connection using Python byte arrays.
    '''

    # for consistency
    def byte_to_int(self, byte):
        '''
        Internal use only.
        '''
        return int.from_bytes(byte, 'little')

    # for consistency
    def byte_to_hex(self, byte):
        '''
        Internal use only.
        '''
        return hex(self.byte_to_int(byte))

    # for consistency
    def print_resp(self, resp):
        '''
        Internal use only.
        '''
        print(':'.join([self.byte_to_hex(x) for x in resp]))

    # Iterate through the byte array and send the bytes through the
    # serial port.
    def send_message(self, data):
        '''
        Internal use only.
        '''
        for b in data:
            self.link.write(b)

        # Give the camera a little time to react.
        time.sleep(0.25)

    # Recieve bytes from the serial port into an array. Return the raw
    # array without checking for errors. The caller is responsible for
    # checking to see if an error happened.
    def receive_message(self):
        '''
        Internal use only.
        '''
        x = []
        v = 0
        while v != b'\xff':
            v = self.link.read(1)
            x.append(v)

        return x

    ###########################
    # Public interface
    ###########################
    def __init__(self, device='/dev/ttyUSB0'):
        '''
        Create the camera object.
        '''
        self.device = device
        self.link = serial.Serial(device)

    def close(self):
        '''
        Close the serial link.
        '''
        self.link.close()

    # Get information from the camera
    def get_camid(self):
        '''
        Get the camera ID.

        Resp: 90 50 zz xx 00 yy ff only the zz parameter is relevent.
        '''
        data = [b'\x81', b'\x09', b'\x04', b'\x22', b'\xff']
        self.send_message(data)
        resp = self.receive_message()
        self.camid = self.byte_to_int(resp[2]) & 0x0F
        return self.camid


    def get_swid(self):
        '''
        Get the software ID.

        Resp: 90 50 [1-125 bytes ASCII SWID] ff.
        '''
        data = [b'\x81', b'\x09', b'\x04', b'\x23', b'\xff']
        self.send_message(data)
        resp = self.receive_message()
        # isolate the return value in the packet
        self.swid = ':'.join([self.byte_to_hex(x) for x in resp[2:39]])
        return self.swid

    def get_hwid(self):
        '''
        Get the hardware ID.

        The response is the Module Serial Number stored
        in EEPROM. The number is converted to ASCII

        Resp: 90 50 [12 bytes ASCII HWID] ff.
        '''
        data = [b'\x81', b'\x09', b'\x04', b'\x24', b'\xff']
        self.send_message(data)
        resp = self.receive_message()
        # isolate the return value
        self.hwid = ':'.join([self.byte_to_hex(x) for x in resp[2:14]])
        return self.hwid

    def get_zoom_pos(self):
        '''
        Get the current zoom position.

        Resp: 90 50 0p 0q 0r 0s ff: pqrs = zoom position
        '''
        data = [b'\x81', b'\x09', b'\x04', b'\x47', b'\xff']
        self.send_message(data)
        resp = self.receive_message()
        self.print_resp(resp)
        return resp

    # Command the camera to do something
    def reset(self):
        '''
        Reset the position of the camera and re-initialize the motors.
        No parameters.
        '''
        data = [b'\x81', b'\x01', b'\x06', b'\x05', b'\xff']
        self.send_message(data)
        # Check for errors
        resp = self.receive_message()
        if self.byte_to_int(resp[1]) != 0x50:
            raise Exception("error response") # TODO: create exception class
