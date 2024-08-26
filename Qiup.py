from pyftdi.ftdi import Ftdi
import pyftdi.serialext
from api_commands import * 
from api_return_values import *

class Qiup():
    def __init__(self, url=None, debug=False, baudrate=115200):
        self.data = []
        self.url = "ftdi://ftdi:ft-x:DQ00QN2Q/1"
        self.baudrate = baudrate
        self.serial = pyftdi.serialext.serial_for_url(self.url, baudrate=self.baudrate)
        self.STX = b'\x02'
        self.ETX = b'\x03'
        if debug == True:
            self.debug = True
        else:
            self.debug = False
        #if url == None:
        #    self.dev = self.get_avail_dev()
    def get_avail_dev(self):
        dev = Ftdi.list_devices('ftdi:///?')
        if len(dev) == 1:
            print(f"Using device {dev}")
            return dev
        if len(dev) == 0:
            print("Did not Found any Ftdi device...")
        if len(dev) > 1:
            print("Found more than 1 FTDI device:")
            print(dev)
    
    def _send_command(self, command, data=None):
        if data==None:
            command = self.STX + command + self.ETX
        else:
            command = self.STX + command
            for dat in data:
                command = command + bytes(dat)
            command = command + self.ETX
        if self.debug:
            print(f"{command} send")
        self.serial.write(command)
        data = self.serial.read_until(b'\x03')
        if self.debug:
            print(f"{data} received")
        data = data.rstrip(b'\x03').lstrip(b'\x02')
        if data[0] == ord(QIU_COMMAND_REJECT_CONF):
            self.check_reject(data[1:])
        return data
    
    def check_connection(self, state):
        match state:
            case 0:
                print("No connection with QIU+")
            case 1:
                print("Connected with USB.")
            case 2:
                print("Connected with Bluetooth.")

    def api_return(self, value):
        match value:
            case 0:
                print("QP_API_SUCCESS")
            case 1:
                print("QP_API_ERROR")
            case 2:
                print("QP_API_ERROR_CMD_UNKNOW")
            case 3:
                print("QP_API_ERROR_HEX_CONVERTER")
            case 4:
                print("QP_API_ERROR_FLASH_SECTOR_RANGE_MIN")
            case 5:
                print("QP_API_ERROR_FLASH_SECTOR_RANGE_MAX")
            case 6:
                print("QP_API_ERROR_FLASH_SECTOR_APPLPROTECTION_RANGE")
        
        return


    def get_api_version(self):
        version_raw = self._send_command(GET_API_VERSION_REQ)
        if version_raw[0]!= ord(GET_API_VERSION_CONF):
            print("Problem with API version request!")
        version_raw = version_raw
        major = version_raw[1:5]
        minor = version_raw[5:9]
        patch = version_raw[9:13]
        build = version_raw[13:17]
        version_string = f"{int(major, 16)}.{int(minor, 16)}.{int(patch, 16)}.{int(build, 16)}"
        print(f"API version on device : {version_string}")
        return version_string
        
    def get_appl_version(self):
        version_raw = self._send_command(GET_APPL_VERSION_REQ)
        if version_raw[0] != ord(GET_APPL_VERSION_CONF):
            print("Problem with Application version request!")
        major = version_raw[1:5]
        minor = version_raw[5:9]
        patch = version_raw[9:13]
        build = version_raw[13:17]
        version_string = f"{int(major, 16)}.{int(minor, 16)}.{int(patch, 16)}.{int(build, 16)}"
        print(f"Application version: {version_string}")
        return version_string

    def register(self ):
        if self.debug:
            answer = self._send_command(QIU_REGISTER_REQ, [1])
        else:
            answer = self._send_command(QIU_REGISTER_REQ, [0])
        if answer[0] != ord(QIU_REGISTER_CONF):
            print("Problem registering QIUP.")
        state = answer[1:3]
        connect_state = int(answer[3:], 16)
        self.api_return(int(state, 16))
        match connect_state:
            case 0:
                print("No Connection with QIU+.")
            case 1:
                print("Connected with USB.")
            case 2:
                print("Connected with Bluetooth.")
        return connect_state

    def release(self):
        answer = self._send_command(QIU_RELEASE_REQ)
        if answer[0] != ord(QIU_RELEASE_CONF):
            print("Problem while releasing communication!")
        state = answer[1:3]
        connect_state = int(answer[3:], 16)
        self.api_return(state)
        self.check_connection(connect_state)
        return connect_state
    
    def trigger_reject(self):
        self._send_command(b'\x01')
    


    def check_reject(self, answer):
        state = int(answer[:2], 16)
        connect_state = int(answer[2:4], 16)
        cmd_state = int(answer[4:6], 16)
        command = answer[6:]
        print("------------------------------")
        print(f"Wrong API command {command}")
        self.api_return(state)
        self.check_connection(connect_state)
        print("------------------------------")
