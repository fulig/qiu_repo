import serial
import serial.tools
import serial.tools.list_ports
import time
from api_commands import *
import numpy as np

dev = '/dev/ttyUSB0'

ser = serial.Serial(dev, baudrate=115200)

def write_cmd(cmd):
    ser.write(b'\x02'+cmd +b'\x03')
    data = ser.read_until(b'\x03')
    return data

send_reg = bytearray(QIU_REGISTER_REQ)
send_reg.extend(b'\x30')
send_reg.append(ord(str(0)))
register = write_cmd(send_reg)

print(register.rstrip(b'\x03').lstrip(b'\x02'))

LED_vector= [1,1,1,0,1,0,1,1]
send_reg = bytearray(LEDBAR_CONTROL_REQ)
[number] = np.packbits(LED_vector)
led_byte = f"{number:02X}"
send_reg.extend(map(ord,led_byte))
time.sleep(1)
led = write_cmd(send_reg)
LED_vector= [0,0,0,0,0,0,0,0]
send_reg = bytearray(LEDBAR_CONTROL_REQ)
[number] = np.packbits(LED_vector)
led_byte = f"{number:02X}"
send_reg.extend(map(ord,led_byte))

[mode] = np.packbits([0,0,0,0,0, 0,1, 1])
send_reg = bytearray(PULSE_MEAS_CONTROL_REQ)
mode = f"{mode:02X}"
send_reg.extend(map(ord, mode))
start_meas = write_cmd(send_reg)
print(start_meas)

send_reg = bytearray(POWER_CONTROL_REQ)
send_reg.extend(b'\x30')
send_reg.append(ord(str(1)))
send_reg.extend(b'\x30')
send_reg.append(ord(str(5)))

for i in range(100):
    data = ser.read_until(b'\x03')
    data = data.rstrip(b'\x03').lstrip(b'\x02\x1d').hex()
    print(data)
    if i == 50:
        power = write_cmd(send_reg)
        print(power)
    

[mode] = np.packbits([0,0,0,0,0, 0,1, 0])
send_reg = bytearray(PULSE_MEAS_CONTROL_REQ)
mode = f"{mode:02X}"
send_reg.extend(map(ord, mode))
stop_meas = write_cmd(send_reg)
print(stop_meas)