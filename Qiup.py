from pyftdi.ftdi import Ftdi
import pyftdi.serialext
import numpy as np
from api_commands import * 
from voltages import *

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
    
    def q_print(self, message):
        print(f"QIUP : {message}")
    
    def get_avail_dev(self):
        dev = Ftdi.list_devices('ftdi:///?')
        if len(dev) == 1:
            self.q_print(f"Using device {dev}")
            return dev
        if len(dev) == 0:
            self.q_print("Did not Found any Ftdi device...")
        if len(dev) > 1:
            self.q_print("Found more than 1 FTDI device:")
            print(dev)
    
    def check_reject(self, answer):
        state = int(answer[:2], 16)
        connect_state = int(answer[2:4], 16)
        cmd_state = int(answer[4:6], 16)
        command = answer[6:]
        self.q_print("------------------------------")
        print(f"Wrong API command {command}")
        self.api_return(state)
        self._check_connection(connect_state)
        self.q_print("------------------------------")

    def send_command(self, command):
        command = self.STX + command + self.ETX
        self.serial.write(command)
        data = self.serial.read_until(b'\x03')
        if self.debug:
            self.q_print(f"{command} send")
            self.q_print(f"{data} received")
        data = data.rstrip(b'\x03').lstrip(b'\x02')
        if data[0] == ord(QIU_COMMAND_REJECT_CONF):
            self.check_reject(data[1:])
        return data
    
    def _check_connection(self, state):
        match state:
            case 0:
                self.q_print("No connection with QIU+")
            case 1:
                self.q_print("Connected with USB.")
            case 2:
                self.q_print("Connected with Bluetooth.")

    def api_return(self, value):
        match value:
            case 0:
                self.q_print("QP_API_SUCCESS")
            case 1:
                self.q_print("QP_API_ERROR")
            case 2:
                self.q_print("QP_API_ERROR_CMD_UNKNOW")
            case 3:
                self.q_print("QP_API_ERROR_HEX_CONVERTER")
            case 4:
                self.q_print("QP_API_ERROR_FLASH_SECTOR_RANGE_MIN")
            case 5:
                self.q_print("QP_API_ERROR_FLASH_SECTOR_RANGE_MAX")
            case 6:
                self.q_print("QP_API_ERROR_FLASH_SECTOR_APPLPROTECTION_RANGE")
        return value
    
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
    
    def convert_voltage(self, voltage):
        voltage_string = ""
        match voltage:
            case 0:
                voltage_string = "Undefined voltage"
            case 1:
                voltage_string = "ACCU_VOLTAGE"
            case 2:
                voltage_string = "USB_VOLTAGE" 
            case 3: 
                voltage_string = "DIG_SUPPLY_VOLTAGE"
            case 4:
                voltage_string = "LED_SUPPLY_VOLTAGE"
            case 5:
                voltage_string = "ANALOG_SUPPLY_VOLTAGE"
            case 6:
                voltage_string  = "CC1DC_VOLTAGE"
            case _:
                voltage = ""
        return voltage_string
    
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
            self.q_print("Error requesting API version.")
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
            self.q_print("Error with Application version request!")
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
                    self.q_print("No Connection with QIU+.")
                case 1:
                    self.q_print("Connected with USB.")
                case 2:
                    self.q_print("Connected with Bluetooth.")
            return  state
        else:
            self.q_print("Error registering QIUP.")
            return None

    def release(self):
        answer = self.send_command(QIU_RELEASE_REQ)
        if answer[0] == ord(QIU_RELEASE_CONF):
            state = answer[1:3]
            connect_state = int(answer[3:], 16)
            self.api_return(state)
            self._check_connection(connect_state)
            return connect_state
        else:
            self.q_print("Error while releasing communication!")
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
            self._check_connection(connect_state)
            if time_remaining == 255:
                self.q_print("More than 2.5 s remaining until release.")
            else:
                print(f"{(time_remaining * 8 )/1024} secounds until Release.")
            return time_remaining
        else:
            self.q_print("Error while retriggering.")
            return None

    def control_power(self, state, voltage_select):
        if state not in [1,0]:
            self.q_print("Wrong state, Use 0 (OFF) or 1 (ON)]")
            return None
        avail_voltage = [QP_API_ANALOG_SUPPLY_VOLTAGE,QP_API_LED_SUPPLY_VOLTAGE]
        if voltage_select in avail_voltage:
            send_reg = bytearray(POWER_CONTROL_REQ)
            send_reg.extend(b'\x30')
            send_reg.append(ord(str(state)))
            send_reg.extend(b'\x30')
            send_reg.append(ord(str(voltage_select)))
            answer = self.send_command(send_reg)
            if answer[0] == ord(POWER_CONTROL_CONF):
                power_return = int(chr(answer[2]))
                power_string = self.convert_voltage(power_return)
                if state == 0:
                    self.q_print(f"Turned OFF {power_string}.")
                if state == 1:
                    self.q_print(f"Turned ON {power_string}.")
                return power_return
            else:
                self.q_print("Error while controlling power.")
                return None
        else:
            print(f"Wrong voltage selection {voltage_select}. Use {avail_voltage}")

    def get_voltage(self, voltage_select):
        avail_voltage = [QP_API_ACCU_VOLTAGE, QP_API_USB_VOLTAGE,QP_API_DIG_SUPPLY_VOLTAGE]
        if voltage_select in avail_voltage:
            send_reg = bytearray(GET_VOLTAGE_REQ)
            send_reg.extend(b'\x30')
            send_reg.append(ord(str(voltage_select)))
            answer = self.send_command(send_reg)
            if answer[0] == ord(GET_VOLTAGE_CONF):
                power_return = int(chr(answer[2]))
                power_string = self.convert_voltage(power_return)
                if self.debug:
                    print(answer)
                voltage = (int(answer[3:].decode(), 16) * 5.0) / 4096 
                self.q_print(f"{power_string} : {voltage}")
                return voltage 
            else:
                print(f"Error while requesting voltage {voltage_select}")
                return None
        else:
            self.q_print(f"Wrong voltage selection. Use {avail_voltage}")
    
    def get_charge_state(self):
        answer = self.send_command(GET_CHARGE_STATE_REQ)
        if answer[0] == ord(GET_CHARGE_STATE_CONF):
            state = self.charge_return(answer[1:3])
            return state
        else:
            self.q_print("Error while requesting charge) state.")
            return None
    
    def control_irled_ext(self, state):
        if state not in [1,0]:
            self.q_print("Wrong state, Use 0 (OFF) or 1 (ON)]")
            return
        send_reg = bytearray(IRLED_EXT_CONTROL_REQ)
        send_reg.extend(b'\x30')
        send_reg.append(ord(str(state)))
        answer = self.send_command(send_reg)
        if answer[0] == ord(IRLED_EXT_CONTROL_CONF):
            if state == 0:
                self.q_print("Turned OFF external IRLED.")
            if state == 1:
                self.q_print("Turned ON external IRLED.")
            return
        else:
            self.q_print("Error with extern IRLED control.")
            return
    
    def control_irled_intern(self, state):
        if state not in [1,0]:
            self.q_print("Wrong state, Use 0 (OFF) or 1 (ON)]")
            return
        send_reg = bytearray(IRLED_INT_CONTROL_REQ)
        send_reg.extend(b'\x30')
        send_reg.append(ord(str(state)))
        answer = self.send_command(send_reg)
        if answer[0] == ord(IRLED_INT_CONTROL_CONF):
            if state == 0:
                self.q_print("Turned OFF internal IRLED.")
            if state == 1:
                self.q_print("Turned ON internal IRLED.")
            return
        else:
            self.q_print("Error with intern IRLED control.")
            return
 
    def dim_led(self, rgb, dim_value):
        rgb = rgb.upper()
        if rgb not in [ "R", "G", "B"]:
            self.q_print("Wrong LED selection use 'R','G' or 'B' (or in lower case)")
        send_reg = bytearray(DIM_LED_REQ)
        rgb_val = hex(ord(rgb))[2:]
        value = f"{dim_value:02X}"
        send_reg.extend(map(ord, rgb_val + value))
        answer = self.send_command(send_reg)
        if answer[0] == ord(DIM_LED_CONF):
            return
        else:
            print(f"Error while dimming {rgb} LED")
            return None
    
    def ledbar_control(self, LED_vector):
        if len(LED_vector) != 8:
            print("Please use list in form of [x,x,x,x,x,x,x,x] -> x=1/0")
        send_reg = bytearray(LEDBAR_CONTROL_REQ)
        [number] = np.packbits(LED_vector)
        led_byte = f"{number:02X}"
        send_reg.extend(map(ord,led_byte))
        answer = self.send_command(send_reg)
        if answer[0] == ord(LEDBAR_CONTROL_CONF):
            self.q_print(f"Setup LED Vector {LED_vector}")
            return led_byte
        else:
            self.q_print("Error while controlling LED Bar.")
            return None

    def check_earclip(self):
        answer = self.send_command(EARCLIP_STATE_REQ)
        if answer[0] == ord(EARCLIP_STATE_CONF):
            state = int(answer[1:], 16)
            if state == 0:
                self.q_print("No Earclip connected")
            if state == 1:
                self.q_print("Earclip connected.")
            return state
        else:
            self.q_print("Error while checking earclip state")
            return None
   
    def read_flash(self, sector_number, part_number):
        send_reg = bytearray(FLASH_READ_DATA_REQ)
        sector = f"{sector_number:04X}"
        part = f"{part_number:02X}"
        send_reg.extend(map(ord, sector+part))
        answer = self.send_command(send_reg)
        if answer[0] == ord(FLASH_READ_DATA_CONF):
            state = int(answer[-2:])
            self.api_return(state)
            data = answer[1:-2]
            return data
        else:
            self.q_print(f"Error while reading flash sector {sector_number}, part {part_number}")
            return None
      
    def write_flash(self, sector_number, part_number, data):
        if not isinstance(data, str):
            self.q_print("Please use string format for data.")
            return
        send_reg = bytearray(FLASH_WRITE_DATA_REQ)
        sector = f"{sector_number:04X}"
        part = f"{part_number:02X}"
        send_reg.extend(map(ord, sector+part))
        send_reg.extend(map(ord, data))
        answer = self.send_command(send_reg)
        if answer[0] == ord(FLASH_WRITE_DATA_CONF):
            state = int(answer[1:])
            self.api_return(state)
            return state
        else:
            self.q_print("Error while writing flash.")
            return None
####### Answer contains more information then written in docu???
    def erase_flash(self, sector_number):
        send_reg = bytearray(FLASH_ERASE_SECTOR_REQ)
        sector = f"{sector_number:04X}"
        send_reg.extend(map(ord, sector))
        answer = self.send_command(send_reg)
        if answer[0] == ord(FLASH_ERASE_SECTOR_CONF):
            state = int(answer[1:3])
            self.api_return(state)
            return state
        else:
            print(f"QIUP: Problem while erasing sector {sector_number}")
            return None

    def puls_measure_control(self, start_stop,online,record,emulation):
        answer = self.send_command(PULSE_MEAS_CONTROL_REQ)
        if answer[0] == ord(PULSE_MEAS_CONTROL_CONF):
            print(answer)
        else:
            self.q_print("Error while setting up Measurement.")
            return None

# No valid API command 0x1E ????
    def get_breathing_rate(self):
        answer = self.send_command(GET_RESP_RATE_REQ)
        if answer[0] == ord(GET_RESP_RATE_CONF):
            breathing_rate = int(answer[1:], 16)
            print(f"QIUP : Breathing rate {breathing_rate + 5}")
            return breathing_rate
        else:
            self.q_print("Error while requesting breathing rate.")
            return None
    
    def set_breathing_rate(self):
        answer = self.send_command(SET_RESP_RATE_REQ)
        if answer[0] == ord(SET_RESP_RATE_CONF):
            breathing_rate = int(answer[1:], 16)
            print(f"QIUP : Breathing rate {breathing_rate + 5}")
        else:
            self.q_print("Error while requesting breathing rate.")
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
            self.q_print("Error while requesting gain stage.")
            return None