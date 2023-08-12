#!/usr/bin/env python3
# https://coderslegacy.com/python/ctypes-tutorial/

import serial
import time

SPEED = 0x18
RESP_DELAY = 0.75
MSG_DELAY = 0.75

# Note that the camera does not like to be moved to its max extents.
MAX_PAN = 800
MIN_PAN = 0
MAX_TILT = 200
MIN_TILT = 0
MAX_ZOOM = 2880
MIN_ZOOM = 0
RESET_PAN = 410
RESET_TILT = 210
RESET_ZOOM = 0
'''
Need to do something about the situation where the value of an input exceeds the
maximum allowable value.
'''

# exception thrown when error = 0x01
class CameraMessageLengthError(Exception):
    '''
    Camera message length exception.
    '''
    def __init__(self):
        self.message = "Camera message length is invalid."
        super().__init__(self.message)

# Returned when the command format is different or when a command with
# illegal command parameters is accepted.
#
# exception thrown when error = 0x02
class CameraSyntaxError(Exception):
    '''
    Camera message syntax error.
    '''
    def __init__(self):
        self.message = "Camera message syntax is invalid."
        super().__init__(self.message)

# Could not accept a command that is received while two commands are
# currently being executed (two sockets have been used).
#
# exception thrown when error = 0x03
class CameraBufferFullError(Exception):
    '''
    Camera buffer full error.
    '''
    def __init__(self):
        self.message = "Camera message buffer is full."
        super().__init__(self.message)

# Returned when a command which is being executed in a socket specified by
# the cancel command is cancelled. The completion message for the command
# is not returned.
#
# exception thrown when error = 0x04
class CameraCancelError(Exception):
    '''
    Camera error while canceling a message.
    '''
    def __init__(self):
        self.message = "Camera message cancel failed."
        super().__init__(self.message)

# Returned when no command is executed in a socket specified by the cancel
# command, or when an invalid socket number is specified.
#
# exception thrown when error = 0x05
class CameraAddressError(Exception):
    '''
    Camera address is invalid.
    '''
    def __init__(self):
        self.message = "Camera address is invalid."
        super().__init__(self.message)

# exception thrown when error = 0x041
class CameraCommandError(Exception):
    '''
    Camera command is invalid.
    '''
    def __init__(self):
        self.message = "Camera command message is invalid."
        super().__init__(self.message)

# Returned when a command cannot be executed due to current conditions.
# For example, when a command for controlling the manual focus is received
# during the auto focus mode.
#
# exception thrown when error = 0x041
class CameraUnknownError(Exception):
    '''
    Camera command is invalid.
    '''
    def __init__(self):
        self.message = "Unknown error response from camera."
        super().__init__(self.message)

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
    def print_msg(self, msg):
        '''
        Internal use only.
        '''
        print(':'.join([self.byte_to_hex(x) for x in msg]))

    # Decode a word in a message received from the camera and return is as an
    # integer.
    def decode_word(self, message, index=2):
        '''
        Internal use only.
        '''
        val = 0
        shift = 12
        for x in message[index:index+4]:
            val |= (self.byte_to_int(x) << shift)
            shift -= 4

        return val

    # Encode a word in a message from an integer.
    def encode_word(self, message, value, index=2):
        '''
        Internal use only.
        '''
        mask = 0xF000
        idx = 12
        value = value & 0xFFFF

        for i in range(index, index+4):
            val = (value & mask) >> idx
            message[i] = val.to_bytes(1, 'little')
            mask = mask >> 4
            idx -= 4

        return message

    # Decode a short (16 bits) in a message received from the camera and return is as an
    # integer.
    def decode_short(self, message, index=4):
        '''
        Internal use only.
        '''
        val = 0
        shift = 4
        for x in message[index:index+2]:
            val |= (self.byte_to_int(x) << shift)
            shift -= 4

        return val

    # Encode a short (16 bits) in a message from an integer.
    def encode_short(self, message, value, index=4):
        '''
        Internal use only.
        '''
        for i in range(index, index+2):
            message[i] = value.to_bytes(1, 'little')

        return message

    # Decode a byte from the given response.
    def decode_byte(self, message, index):
        '''
        Internal use only.
        '''
        return self.byte_to_int(message[index])

    # Encode a byte into the message at the given index.
    def encode_byte(self, message, value, index):
        '''
        Internal use only.
        '''
        message[index] = value.to_bytes(1, 'little')

    # Iterate through the byte array and send the bytes through the
    # serial port.
    def send_message(self, data, siz):
        '''
        Internal use only.
        '''
        print("send:", self.link.in_waiting, ",", self.link.out_waiting)
        # Sometimes the camera sends a push message that is not a response to
        # a message that we sent. This eats those safely.
        if self.link.in_waiting != 0:
            m = self.receive_message(self.link.in_waiting)
            self.print_msg(m)

        self.print_msg(data)
        for b in data:
            self.link.write(b)
        self.link.flush()

        return self.receive_message(siz)


    # Receive bytes from the serial port into an array. Return the raw
    # array without checking for errors. The caller is responsible for
    # checking to see if an error happened.
    def receive_message(self, siz):
        '''
        Internal use only.
        '''
        print("receive:", self.link.in_waiting, ",", self.link.out_waiting)
        x = []
        v = 0
        while self.link.in_waiting < siz:
            time.sleep(0.1)

        for i in range(self.link.in_waiting):
            v = self.link.read(1)
            x.append(v)

        self.print_msg(x)
        return x

    # Check for an error and raise an exception if one has taken place.
    # Otherwise return the raw response for further processing.
    def check_error(self, resp):
        '''
        Internal use only.
        '''
        #resp = self.receive_message()
        #self.print_resp(resp)
        if self.byte_to_int(resp[1]) & 0xF0 != 0x50:
            if self.byte_to_int(resp[2]) & 0xFF == 0x41:
                raise CameraCommandError
            elif self.byte_to_int(resp[2]) & 0x0F == 0x01:
                raise CameraMessageLengthError
            elif self.byte_to_int(resp[2]) & 0x0F == 0x02:
                raise CameraSyntaxError
            elif self.byte_to_int(resp[2]) & 0x0F == 0x03:
                raise CameraBufferFullError
            elif self.byte_to_int(resp[2]) & 0x0F == 0x04:
                raise CameraCancelError
            elif self.byte_to_int(resp[2]) & 0x0F == 0x05:
                raise CameraAddressError

        return resp

    # Verify that the camera is responding to the ping.
    def check_ack(self):
        resp = self.receive_message()
        if self.byte_to_int(resp[1]) & 0xF0 != 0x40:
            raise Exception("bad ping")

    ###########################
    # Public interface
    ###########################
    def __init__(self, device='/dev/ttyUSB0'):
        '''
        Create the camera object.
        '''
        self.device = device
        self.link = serial.Serial(self.device)
        self.reset()
        time.sleep(1)

    def __del__(self):
        '''
        Destroy the camera object.
        '''
        self.reset()
        self.link.close()

    def reboot(self):
        '''
        Reboot the camera and reset all parameters
        '''
        data = [b'\x81', b'\x01', b'\x42', b'\xff']
        self.send_message(data)

    def get_zoom(self):
        '''
        Get the current zoom position.

        Resp: 90 50 0p 0q 0r 0s ff: pqrs = zoom position
        '''
        data = [b'\x81', b'\x09', b'\x04', b'\x47', b'\xff']
        resp = self.send_message(data, 7)
        self.check_error(resp)
        return self.decode_word(resp)

    def get_pos(self):
        '''
        Get the pan and tilt position. Returns a dict where
        {"pan": int, "tilt": int}

        Resp: 90 50 0p 0q 0r 0s 0t 0u 0v 0w ff
        pqrs: pan position
        tuvw: tilt position
        '''
        data = [b'\x81', b'\x09', b'\x06', b'\x12', b'\xff']
        resp = self.send_message(data, 11)
        self.check_error(resp)
        #self.print_resp(resp)
        retv = {}
        retv['pan'] = self.decode_word(resp)
        retv['tilt'] = self.decode_word(resp, index=6)
        #print(retv)
        return retv


    def get_status(self):
        '''
        Return a dictionary with pan, tilt, and zoom values.
        '''
        val = self.get_pos()
        val['zoom'] = self.get_zoom()

        return val


    ################################################
    # Command the camera to do something
    def reset(self):
        '''
        Reset the position of the camera and re-initialize the motors.
        No parameters.
        '''
        data = [b'\x81', b'\x01', b'\x06', b'\x05', b'\xff']
        self.send_message(data, 0)
        self.check_error(self.receive_message(3))
        #time.sleep(2)

    def zoom_in(self):
        '''
        Zoom in to the maximum extent

        8x 01 04 07 2p ff
        p = speed parameter, a (low) to b (high)

        max zoom = 2885
        '''
        data = [b'\x81', b'\x01', b'\x04', b'\x07', b'\x2f', b'\xff']
        self.send_message(data, 3)

    def zoom_out(self):
        '''
        Zoom out to the maximum extent

        8x 01 04 07 3p ff
        p = speed parameter, a (low) to b (high)

        min zoom = 0
        '''
        data = [b'\x81', b'\x01', b'\x04', b'\x07', b'\x3f', b'\xff']
        self.send_message(data, 3)

    def move_up(self, pan=SPEED, tilt=SPEED):
        '''
        Set the speed when the camera moves up and move it to the limit.
        8x 01 06 01 vv ww 03 01 FF
        vv = pan speed 01 - 18
        ww = tilt speed 01 - 18

        max tilt = 210
        '''
        data = [b'\x81', b'\x01', b'\x06', b'\x01',
                b'\x01', b'\x01', b'\x03', b'\x01', b'\xFF']
        self.encode_byte(data, pan, 4)
        self.encode_byte(data, tilt, 5)
        self.send_message(data, 3)

    def move_down(self, pan=SPEED, tilt=SPEED)        :
        '''
        Set the speed when the camera moves down and move it to the limit.
        8x 01 06 01 vv ww 03 01 FF
        vv = pan speed 01 - 18
        ww = tilt speed 01 - 18

        min tilt = 0
        '''
        data = [b'\x81', b'\x01', b'\x06', b'\x01',
                b'\x01', b'\x01', b'\x03', b'\x02', b'\xFF']
        self.encode_byte(data, pan, 4)
        self.encode_byte(data, tilt, 5)
        self.send_message(data, 3)

    def move_left(self, pan=SPEED, tilt=SPEED):
        '''
        Set the speed when the camera moves left and move it to the limit.
        8x 01 06 01 vv ww 03 01 FF
        vv = pan speed 01 - 18
        ww = tilt speed 01 - 18

        min pan = 0
        '''
        data = [b'\x81', b'\x01', b'\x06', b'\x01',
                b'\x01', b'\x01', b'\x01', b'\x03', b'\xFF']
        self.encode_byte(data, pan, 4)
        self.encode_byte(data, tilt, 5)
        self.send_message(data, 3)

    def move_right(self, pan=SPEED, tilt=SPEED):
        '''
        Set the speed when the camera moves right and move it to the limit.
        8x 01 06 01 vv ww 03 01 FF
        vv = pan speed 01 - 18
        ww = tilt speed 01 - 18

        max pan = 817
        '''
        data = [b'\x81', b'\x01', b'\x06', b'\x01',
                b'\x01', b'\x01', b'\x02', b'\x03', b'\xFF']
        self.encode_byte(data, pan, 4)
        self.encode_byte(data, tilt, 5)
        self.send_message(data, 3)

    def move_stop(self):
        '''
        Set the stop speed
        8x 01 06 01 vv ww 03 03 FF
        vv = pan speed 01 - 18
        ww = tilt speed 01 - 18
        '''
        data = [b'\x81', b'\x01', b'\x06', b'\x01',
                b'\x03', b'\x03', b'\x03', b'\x03', b'\xFF']
        self.send_message(data, 3)

    def set_pos(self, pan, tilt, pspeed=SPEED, tspeed=SPEED):
        '''
        Set the absolute position of the camera.

        8x 01 06 02 0p 0t 0x 0x 0x 0x 0y 0y 0y 0y ff
        p = pan speed (01 - 1f)
        t = pan speed (01 - 1f)
        xxxx = pan position 0 = left & 816 = right
        yyyy = tilt position 0 = up & 89 = down
        '''
        data = [b'\x81', b'\x01', b'\x06', b'\x02',
                b'\x00', b'\x00',
                b'\x00', b'\x00', b'\x00', b'\x00',
                b'\x00', b'\x00', b'\x00', b'\x00',
                b'\xff']

        self.encode_byte(data, pspeed, 4)
        self.encode_byte(data, tspeed, 5)
        self.encode_word(data, pan, 6)
        self.encode_word(data, tilt, 10)
        #self.print_msg(data)
        self.send_message(data, 3)
        #self.check_error()

    def set_zoom(self, val):
        '''
        Set the zoom position

        8x 01 04 47 0p 0q 0r 0s ff
        pqrs: zoom position
        '''
        data = [b'\x81', b'\x01', b'\x04', b'\x47',
                b'\x00', b'\x00', b'\x00', b'\x00',
                b'\xff']
        self.encode_word(data, val, 4)
        self.send_message(data, 3)
        #self.check_error(self.receive_message(3))

    def set_all(self, pan, tilt, zoom, pspeed=SPEED, tspeed=SPEED):
        '''
        Set the pan, tilt, and zoom with one message.
        '''
        data = [b'\x81', b'\x01', b'\x06', b'\x02',
                b'\x00', b'\x00',
                b'\x00', b'\x00', b'\x00', b'\x00',
                b'\x00', b'\x00', b'\x00', b'\x00',
                b'\xff',
                b'\x81', b'\x01', b'\x04', b'\x47',
                b'\x00', b'\x00', b'\x00', b'\x00',
                b'\xff']
        self.encode_byte(data, pspeed, 4)
        self.encode_byte(data, tspeed, 5)
        self.encode_word(data, pan, 6)
        self.encode_word(data, tilt, 10)
        self.encode_word(data, zoom, 19)
        self.send_message(data, 6)

    def get_device(self):
        return self.device