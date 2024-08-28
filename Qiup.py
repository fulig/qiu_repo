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
            print("QIUP : Did not Found any Ftdi device...")
        if len(dev) > 1:
            print("QIUP : Found more than 1 FTDI device:")
            print(dev)
    
    def check_reject(self, answer):
        state = int(answer[:2], 16)
        connect_state = int(answer[2:4], 16)
        cmd_state = int(answer[4:6], 16)
        command = answer[6:]
        print("QIUP : ------------------------------")
        print(f"Wrong API command {command}")
        self.api_return(state)
        self.check_connection(connect_state)
        print("QIUP : ------------------------------")

    def send_command(self, command):
        command = self.STX + command + self.ETX
        self.serial.write(command)
        data = self.serial.read_until(b'\x03')
        if self.debug:
            print(f"QIUP : {command} send")
            print(f"QIUP : {data} received")
        data = data.rstrip(b'\x03').lstrip(b'\x02')
        if data[0] == ord(QIU_COMMAND_REJECT_CONF):
            self.check_reject(data[1:])
        return data
    
    def check_connection(self, state):
        match state:
            case 0:
                print("QIUP : No connection with QIU+")
            case 1:
                print("QIUP : Connected with USB.")
            case 2:
                print("QIUP : Connected with Bluetooth.")

    def api_return(self, value):
        match value:
            case 0:
                print("QIUP : QP_API_SUCCESS")
            case 1:
                print("QIUP : QP_API_ERROR")
            case 2:
                print("QIUP : QP_API_ERROR_CMD_UNKNOW")
            case 3:
                print("QIUP : QP_API_ERROR_HEX_CONVERTER")
            case 4:
                print("QIUP : QP_API_ERROR_FLASH_SECTOR_RANGE_MIN")
            case 5:
                print("QIUP : QP_API_ERROR_FLASH_SECTOR_RANGE_MAX")
            case 6:
                print("QIUP : QP_API_ERROR_FLASH_SECTOR_APPLPROTECTION_RANGE")
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
        if version_raw[0]== ord(GET_API_VERSION_CONF):
            version_raw = version_raw
            major = version_raw[1:5]
            minor = version_raw[5:9]
            patch = version_raw[9:13]
            build = version_raw[13:17]
            version_string = f"{int(major, 16)}.{int(minor, 16)}.{int(patch, 16)}.{int(build, 16)}"
            print(f"QIUP : API version on device {version_string}")
            return version_string
        else:
            print("QIUP : Error requesting API version.")
            return None
        
    def get_appl_version(self):
        version_raw = self.send_command(GET_APPL_VERSION_REQ)
        if version_raw[0] == ord(GET_APPL_VERSION_CONF):
            major = version_raw[1:5]
            minor = version_raw[5:9]
            patch = version_raw[9:13]
            build = version_raw[13:17]
            version_string = f"{int(major, 16)}.{int(minor, 16)}.{int(patch, 16)}.{int(build, 16)}"
            print(f"QIUP : Application version {version_string}")
            return version_string
        else:
            print("QIUP : Error with Application version request!")
            return None

    def register(self, mode=0 ):
        send_reg = bytearray(QIU_REGISTER_REQ)
        send_reg.extend(b'\x30')
        send_reg.append(ord(str(mode)))
        answer = self.send_command(send_reg)
        if answer[0] == ord(QIU_REGISTER_CONF):
            state = int(answer[1:3],16)
            connect_state = int(answer[3:], 16)
            self.api_return(state)
            match connect_state:
                case 0:
                    print("QIUP : No Connection with QIU+.")
                case 1:
                    print("QIUP : Connected with USB.")
                case 2:
                    print("QIUP : Connected with Bluetooth.")
            return  state
        else:
            print("QIUP : Error registering QIUP.")
            return None

    def release(self):
        answer = self.send_command(QIU_RELEASE_REQ)
        if answer[0] == ord(QIU_RELEASE_CONF):
            state = answer[1:3]
            connect_state = int(answer[3:], 16)
            self.api_return(state)
            self.check_connection(connect_state)
            return connect_state
        else:
            print("QIUP : Error while releasing communication!")
            return None
        
    def _trigger_reject(self):
        self.send_command(b'\x01')
        
    def register_retrigger(self):
        answer = self.send_command(QIU_REGISTER_RETRIGGER_REQ)
        if answer[0] == ord(QIU_REGISTER_RETRIGGER_CONF):
            state = answer[1:3]
            connect_state = int(answer[3:5])
            time_remaining = int(answer[5:], 16)
            self.api_return(state)
            self.check_connection(connect_state)
            if time_remaining == 255:
                print("QIUP : More than 2.5 s remaining until release.")
            else:
                print(f"{(time_remaining * 8 )/1024} secounds until Release.")
            return time_remaining
        else:
            print("QIUP : Error while retriggering.")
            return None
##########################################################################
# Not working!?
    def control_power(self, state, voltage_select):
        answer = self.send_command(POWER_CONTROL_REQ, [state, voltage_select])
        if answer[0] == ord(POWER_CONTROL_CONF):
            power_return = answer[1:]
            print(power_return)

        else:
            print("QIUP : Error while controlling power.")
            return None
    
    def get_voltage(self, voltage_select):
        answer = self.send_command(GET_VOLTAGE_REQ, [voltage_select])
        if answer[0] == ord(GET_VOLTAGE_CONF):
            print(answer)
        else:
            print(f"Error while requesting voltage {voltage_select}")
            return None
####################################################################
    
    def get_charge_state(self):
        answer = self.send_command(GET_CHARGE_STATE_REQ)
        if answer[0] == ord(GET_CHARGE_STATE_CONF):
            state = self.charge_return(answer[1:3])
            return state
        else:
            print("QIUP : Error while requesting charge) state.")
            return None
    
    def control_irled_ext(self, state):
        answer = self.send_command(IRLED_EXT_CONTROL_REQ, [state])
        if answer[0] == ord(IRLED_EXT_CONTROL_CONF):
            print(answer)
        else:
            print("QIUP : Error with extern IRLED control.")
            return None
    
    def control_irled_intern(self, state):
        answer = self.send_command(IRLED_INT_CONTROL_REQ, [state])
        if answer[0] == ord(IRLED_INT_CONTROL_CONF):
            print(answer)
        else:
            print("QIUP : Error with extern IRLED control.")
            return None
##########################################################
# NOT WORKING  
    def dim_led(self, rgb, dim_value):
        answer = self.send_command(DIM_LED_REQ, [ord(rgb), dim_value])
        print(answer)
        if answer[0] == ord(DIM_LED_CONF):
            print(answer)
        else:
            print(f"Error while dimming {rgb} LED")
            return None
    
    def ledbar_control(self, LED_vector):
        answer = self.send_command(LEDBAR_CONTROL_REQ, [LED_vector])
        if answer[0] == ord(LEDBAR_CONTROL_CONF):
            print(answer)
        else:
            print("QIUP : Error while controlling LED Bar.")
            return None
################################################################

    def check_earclip(self):
        answer = self.send_command(EARCLIP_STATE_REQ)
        if answer[0] == ord(EARCLIP_STATE_CONF):
            state = int(answer[1:], 16)
            if state == 0:
                print("QIUP : No Earclip connected")
            if state == 1:
                print("QIUP : Earclip connected.")
            return state
        else:
            print("QIUP : Error while checking earclip state")
            return None
################################################################
# Needs furthermore tests.    
    def read_flash(self, sector_number, part_number):
        sector = sector_number.to_bytes(2)
        answer = self.send_command(FLASH_READ_DATA_REQ, [sector[0], sector[1], part_number])
        print(answer)
        if answer[0] == ord(FLASH_READ_DATA_CONF):
            print(answer)
        else:
            print(f"QIUP : Error while reading flash sector {sector_number}, part {part_number}")
            return None
        
    def write_flash(self, sector_h, sector_l, part_number, data):
        command_data = [sector_h, sector_l, part_number]
        for b in data:
            command_data.append(b)
        answer = self.send_command(FLASH_WRITE_DATA_REQ, command_data)
        if answer[0] == ord(FLASH_WRITE_DATA_CONF):
            print(answer)
        else:
            print("QIUP : Error while writing flash.")
            return None


    def erase_flash(self, sector_number):
        sector = sector_number.to_bytes(2)
        answer = self.send_command(FLASH_ERASE_SECTOR_REQ, [sector[0], sector[1]])
        if answer[0] == ord(FLASH_ERASE_SECTOR_CONF):
            print(answer)
        else:
            print(f"QIUP: Problem while erasing sector {sector_number}")
            return None

    def puls_measure_control(self, start_stop,online,record,emulation):
        answer = self.send_command(PULSE_MEAS_CONTROL_REQ)
        if answer[0] == ord(PULSE_MEAS_CONTROL_CONF):
            print(answer)
        else:
            print("QIUP : Error while setting up Measurement.")
            return None
###########################################################################

# No valid API command 0x1E ????
    def get_breathing_rate(self):
        answer = self.send_command(GET_RESP_RATE_REQ)
        if answer[0] == ord(GET_RESP_RATE_CONF):
            breathing_rate = int(answer[1:], 16)
            print(f"QIUP : Breathing rate {breathing_rate + 5}")
            return breathing_rate
        else:
            print("QIUP : Error while requesting breathing rate.")
            return None
    
    def set_breathing_rate(self):
        answer = self.send_command(SET_RESP_RATE_REQ)
        if answer[0] == ord(SET_RESP_RATE_CONF):
            breathing_rate = int(answer[1:], 16)
            print(f"QIUP : Breathing rate {breathing_rate + 5}")
        else:
            print("QIUP : Error while requesting breathing rate.")
            return None
    
    def get_gain(self):
        answer = self.send_command(GET_GAIN_REQ)
        if answer[0] == ord(GET_GAIN_CONF):
            gain_state = int(answer[1:], 16)

            match gain_state:
                case 0:
                    gain = "479 (53.6 dB)"
                case 1:
                    gain = "1277 (62.1 dB)"
                case 2:
                    gain = "2553 (68.1 dB)"
                case 3:
                    gain = "4096 (72.2 dB)"
            print(f"Verstärkung {gain}.")
            return gain_state
        else:
            print("QIUP : Error while requesting gain stage.")
            return None