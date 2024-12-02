import serial
import serial.tools.list_ports
from api_commands import * 
from voltages import *
import numpy as np
import re
import datetime


class Qiup():
    def __init__(self, url=None, debug=False, baudrate=115200):
        self.baudrate = baudrate
        self.port = self.get_avail_dev()
        self.STX = b'\x02'
        self.ETX = b'\x03'
        self.run_idx = 0
        self.ex_run_idx = 0
        self.inc = True

        self.debug = debug
        #self.url, self.name = self.get_avail_dev()

    def setup_serial(self):
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate,timeout=4)
        return
    
    def get_avail_dev(self):
        ports = serial.tools.list_ports.comports()
        if not ports:
            self.q_print("No serial devices connected.")
            return None
        else:
            usb_ports = []
            for port in ports:
                if "ttyUSB" in port.device:
                    self.q_print(f"Found serial device: {port.device}")
                    usb_ports.append(port)
            # Return the first available port
            return usb_ports[0].device
    
    def close_serial(self):
        self.serial.close()

    def q_print(self, message):
        print(f"QIUP : {message}")


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
        if data == b'':
            self.q_print("Could not register with Qiup+. Maybe turned OFF?")
            return None
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
        if answer == None:
            return
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
            return  connect_state
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

    def write_flash(self, sector_number, part_number, data, api_return=True):
        if not isinstance(data, str):
            self.q_print("Please use string format for data.")
            return
        data = data.upper()
        send_reg = bytearray(FLASH_WRITE_DATA_REQ)
        sector = f"{sector_number:04X}"
        part = f"{part_number:02X}"
        send_reg.extend(map(ord, sector+part))
        send_reg.extend(map(ord, data))
        answer = self.send_command(send_reg)
        if answer[0] == ord(FLASH_WRITE_DATA_CONF):
            state = int(answer[1:])
            if api_return:
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

    def puls_measure_control(self, emulation, record, online, start_stop):
        [mode] = np.packbits([0,0,0,0,emulation, record,online, start_stop])
        send_reg = bytearray(PULSE_MEAS_CONTROL_REQ)
        mode = f"{mode:02X}"
        send_reg.extend(map(ord, mode))
        answer = self.send_command(send_reg)
        if answer[0] == ord(PULSE_MEAS_CONTROL_CONF):
            if start_stop == 0:
                self.q_print("Measurement stopped.")
            if start_stop == 1:
                self.q_print("Measurement started.")
        else:
            self.q_print("Error while setting up Measurement.")
            return None
    
    def start_measure(self):
        self.puls_measure_control(0,0,1,1)
        return
    
    def stop_measure(self):
        self.puls_measure_control(0,0,0,0)
        self.inc = True
        self.run_idx = 1
        return

    def get_measurement_data(self):
        data = self.serial.read_until(b'\x03')
        if data[1] == ord(PULSE_MEAS_DATA_16_IND):
            
            data = data.rstrip(b'\x03').lstrip(b'\x02\x1d').hex()
            data_list = []
            data_len = int(data[:4],16)
            data = data[4:]
            if data_len > 34:
                if self.debug:
                    print("Repairing data...")
                data = re.sub("ff0[a-fA-F0-9]{3}","", data)
            for i in range(int(len(data)/4)):
                b_data = data[i*4:(i+1)*4]
                swap = b_data[2:] + b_data[:2]
                received = swap[0]
                right_value = int(swap, 16) & 0x0FFF
                data_list.append(right_value)
                self.handle_idx()
            return data_list

    def fix_data(self,data_line):
        
        #self.handle_idx()
        return_data = []
        return_data[:0] = data_line
        print(len(data_line))
        
         # ''.join(return_data)
        #print("--------")
        #print(data_line)
        #print(return_data)
        #print("--------")
        return return_data
    
    def handle_idx(self):
        if self.inc:
            self.run_idx += 1
        else:
            self.run_idx -= 1
        if self.run_idx == 7:
            self.inc = False
        if self.run_idx == 1:
            self.inc = True
        #print(f"IDX : {self.run_idx}")

    def print_gain(self, gain_stage):
        gain = ""
        match gain_stage:
                case 0:
                    gain = "479 (53.6 dB)"
                case 1:
                    gain = "1277 (62.1 dB)"
                case 2:
                    gain = "2553 (68.1 dB)"
                case 3:
                    gain = "4096 (72.2 dB)"
        return gain
    
    def get_gain(self):
        answer = self.send_command(GET_GAIN_REQ)
        if answer[0] == ord(GET_GAIN_CONF):
            gain_stage = int(answer[1:], 16)
            gain = self.print_gain(gain_stage)
            print(f"Gain is {gain}.")
            return gain_stage
        else:
            self.q_print("Error while requesting gain stage.")
            return None
    
    def set_gain(self, stage):
        if stage > 3:
            self.q_print("Max gain stage is 3")
            return
        send_reg = bytearray(SET_GAIN_REQ)
        set_gain = f"{stage:02X}"
        send_reg.extend(map(ord, set_gain))
        answer = self.send_command(send_reg)
        if answer[0] == ord(SET_GAIN_CONF):
            gain_stage = self.print_gain(stage)
            self.q_print(f"Set gain to {gain_stage}")
            return set_gain
        else:
            self.q_print("Error while requesting gain stage.")
            return None
    
    def convert_datetime(self, raw_time):
        year =  str(int(raw_time[0:4],16)).zfill(4)
        month = str(int(raw_time[4:6],16)).zfill(2)
        day = str(int(raw_time[6:8],16)).zfill(2)
        hours = str(int(raw_time[8:10],16)).zfill(2)
        min = str(int(raw_time[10:12], 16)).zfill(2)
        secs = str(int(raw_time[12:], 16)).zfill(2)
        time = [year, month, day, hours, min, secs]
        return time

    def get_datetime(self):
        answer = self.send_command(GET_DATETIME_REQ)
        if answer[0] == ord(GET_DATETIME_CONF):
            time = self.convert_datetime(answer[1:])
            self.q_print(f"{time[0]}-{time[1]}-{time[2]} {time[3]}:{time[4]}:{time[5]}")
            return time
        else:
            self.q_print("Error while requesting date time.")
            return None
    
    def set_datetime(self, datetime):
        year = f"{datetime[0]:04X}"
        month = f"{datetime[1]:02X}"
        day = f"{datetime[2]:02X}"
        hours = f"{datetime[3]:02X}"
        min = f"{datetime[4]:02X}"
        secs = f"{datetime[5]:02X}"
        send_reg = bytearray(SET_DATETIME_REQ)
        send_reg.extend(map(ord, year+month+day+hours+min+secs))
        answer = self.send_command(send_reg)
        if answer[0] == ord(SET_DATETIME_CONF):
            month = f"{datetime[1]}".zfill(2)
            day = f"{datetime[2]}".zfill(2)
            hours = f"{datetime[3]}".zfill(2)
            min = f"{datetime[4]}".zfill(2)
            secs = f"{datetime[5]}".zfill(2)
            self.q_print("Set date time to "
                         +f"{datetime[0]}-{month}-{day} "
                         +f"{hours}:{min}:{secs}"
                         )
            return True
        else:
            self.q_print("Error while setting date time.")
            return None
    
    def set_time_from_pc(self):
        self.q_print("Setting time from PC.")
        pc_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        year = int(pc_time[0:4])
        month = int(pc_time[4:6])
        day = int(pc_time[6:8])
        hours = int(pc_time[8:10])
        min =   int(pc_time[10:12])
        secs =  int(pc_time[12:14])
        self.set_datetime([year,month,day,hours,min,secs])

    def play_sound(self, sound_nr):
        send_reg = bytearray(PLAY_SOUND_REQ)
        sound = f"{sound_nr:02X}"
        send_reg.extend(map(ord,sound))
        answer = self.send_command(send_reg)
        if answer[0] == ord(PLAY_SOUND_CONF):
            print(f"Playing sound {sound_nr}")
            return True
        else:
            self.q_print(f"Error while playing sound {sound_nr}")
            return None
    
    def pushbutton_state(self):
        send_reg = bytearray(PUSHBUTTON_STATE_REQ)
        answer = self.send_command(send_reg)
        if answer[0] == ord(PUSHBUTTON_STATE_CONF):
            state = int(answer[1:])
            if state == 0:
                self.q_print("Button not pressed")
            if state == 1:
                self.q_print("Button pressed")
            return state
        else:
            self.q_print("Error while checking button state")
            return None
    
    def twos_comp(self, val, bits):
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val
    
#Umrechnung implementieren!!!       
    def get_accel(self):
        send_reg = bytearray(GET_ACCEL_RAW_REQ)
        answer = self.send_command(send_reg)
        if answer[0] == ord(GET_ACCEL_RAW_CONF):
            state = int(answer[1:3])
            self.api_return(state)
            if state == 1:
                return ["XXX", "XXX", "XXX"]
            if state == 0:        
                accel_x = int(answer[3:7],16 ) >> 2
                accel_y = int(answer[7:11],16) >> 2
                accel_z = int(answer[11:15], 16) >> 2
                raw_x = self.twos_comp(accel_x, 14) 
                raw_y = self.twos_comp(accel_y , 14)
                raw_z = self.twos_comp(accel_z , 14)                
                x = raw_x * 0.244 / 1000
                y = raw_y * 0.244 / 1000
                z = raw_z * 0.244 / 1000
            return [x,y,z]
        else:
            self.q_print("Error")
            return None