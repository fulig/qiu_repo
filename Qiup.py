from pyftdi.ftdi import Ftdi
import pyftdi.serialext
from api_commands import * 

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
    
    def _send_command(self, command):
        command = self.STX + command + self.ETX
        if self.debug:
            print(f"Sending byte {command}")
        self.serial.write(command)
        data = self.serial.read_until(b'\x03')
        if self.debug:
            print(f"Received : {data}")
        return data
    
    def get_api_version(self):
        version_raw = self._send_command(GET_API_VERSION_REQ)
        version_raw = version_raw.rstrip(b'\x03').lstrip(b'\x02')
        major = version_raw[1:5]
        minor = version_raw[5:9]
        patch = version_raw[9:13]
        build = version_raw[13:17]
        version_string = f"{int(major, 16)}.{int(minor, 16)}.{int(patch, 16)}.{int(build, 16)}"
        #print(f"major : {major}, minor : {minor}, patch : {patch}, build : {build}")
        print(f"API version on device : {version_string}")
        return version_string
        