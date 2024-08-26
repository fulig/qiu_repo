from pyftdi.ftdi import Ftdi
import serial
import pyftdi.serialext
import random
import numpy as np

STX = b'\x02'
ETX = 0x03
ping = 0x70


baudrate = 115200

#Ftdi.show_devices()
#ping_1 = b'\x02p09933DDC9AE1E1\x03'
#ping = b'\x02p5EA0547BFE2F2F\x03'
LED_1 = b'\x02\x0C5\x03'
version = b'\x02\x26\x03'
REGISTER = b'\x02\x32\x00\x03'
RELEASE = b'\x02\x34\x03'
#old_url = ftdi://ftdi:ft-x:DK0HGAC5/1
url = "ftdi://ftdi:ft-x:DQ00QN2Q/1"
port = pyftdi.serialext.serial_for_url(url, baudrate=baudrate)
print(REGISTER)
port.write(REGISTER)
data=port.read_until(b'\x03')
print(data)
print(RELEASE)
port.write(RELEASE)
#data = port.read()
data=port.read_until(b'\x03')
print(data)
port.close()

#generate_unlock_bytes()
