from pyftdi.ftdi import Ftdi
import pyftdi.serialext
from api_commands import * 

class Qiup():
    def __init__(self, url=None, debug=False, baudrate=115200):
        self.data = []
        #self.url = "ftdi://ftdi:ft-x:DQ00QN2Q/1"
        self.url = "ftdi://ftdi:ft-x:DK0HGAC5/1"
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

    def send_command(self, command, data=None):
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
    
    def charge_return(self, state):
        match state:
            case b'0A':
                mode = "No Battery."
            case b'0B':
                mode = "Not Charging"
            case b'0C':
                mode = "PRE/FAST Charging"
            case b'0D':
                mode = "TOP-OFF Charging"
            case b'0E':
                mode = "Maintainance"
            case b'0F':
                mode = "Fault"
        print(f"Charging info : {mode}")
        return state

    def get_api_version(self):
        version_raw = self.send_command(GET_API_VERSION_REQ)
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
        version_raw = self.send_command(GET_APPL_VERSION_REQ)
        if version_raw[0] != ord(GET_APPL_VERSION_CONF):
            print("Problem with Application version request!")
        major = version_raw[1:5]
        minor = version_raw[5:9]
        patch = version_raw[9:13]
        build = version_raw[13:17]
        version_string = f"{int(major, 16)}.{int(minor, 16)}.{int(patch, 16)}.{int(build, 16)}"
        print(f"Application version: {version_string}")
        return version_string

    def register(self, mode=1 ):
        answer = self.send_command(QIU_REGISTER_REQ, [mode])
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
        answer = self.send_command(QIU_RELEASE_REQ)
        if answer[0] != ord(QIU_RELEASE_CONF):
            print("Problem while releasing communication!")
        state = answer[1:3]
        connect_state = int(answer[3:], 16)
        self.api_return(state)
        self.check_connection(connect_state)
        return connect_state
    
    def _trigger_reject(self):
        self.send_command(b'\x01')
        
    def register_retrigger(self):
        answer = self.send_command(QIU_REGISTER_RETRIGGER_REQ)
        if answer[0] != ord(QIU_REGISTER_RETRIGGER_CONF):
            print("Problem while retriggering.")
        state = answer[1:3]
        connect_state = int(answer[3:5])
        time_remaining = int(answer[5:], 16)
        self.api_return(state)
        self.check_connection(connect_state)
        if time_remaining == 255:
            print("More than 2.5 s remaining until release.")
        else:
            print(f"{(time_remaining * 8 )/1024} secounds until Release.")
        return time_remaining

##########################################################################
# Docu überprüfen !! Werte für die unterschiedlichen Voltages nicht vorhande (mit X eingetragen).
    def control_power(self, state, voltage_select):
        answer = self.send_command(POWER_CONTROL_REQ, [state, voltage_select])
        print(answer)
        if answer[0] != POWER_CONTROL_CONF:
            print("Problem while controlling power.")
    
    def get_voltage(self, voltage_select):
        answer = self.send_command(GET_VOLTAGE_REQ, [voltage_select])
        print(answer)
        if answer[0] != ord(GET_VOLTAGE_CONF):
            print(f"Problem while requesting voltage {voltage_select}")
####################################################################
    
    def get_charge_state(self):
        answer = self.send_command(GET_CHARGE_STATE_REQ)
        if answer[0] != ord(GET_CHARGE_STATE_CONF):
            print("Problem while requesting charge) state.")
        self.charge_return(answer[1:3])
    
    def control_irled_ext(self, state):
        answer = self.send_command(IRLED_EXT_CONTROL_REQ, [state])
        if answer[0] != ord(IRLED_EXT_CONTROL_CONF):
            print("Problem with extern IRLED control.")
    
    def control_irled_intern(self, state):
        answer = self.send_command(IRLED_INT_CONTROL_REQ, [state])
        if answer[0] != ord(IRLED_INT_CONTROL_CONF):
            print("Problem with extern IRLED control.")
    
    def dim_led(self, rgb, dim_value):
        answer = self.send_command(DIM_LED_REQ, [ord(rgb), dim_value])
        print(answer)
        if answer[0] != ord(DIM_LED_CONF):
            print(f"Problem while dimming {rgb} LED")