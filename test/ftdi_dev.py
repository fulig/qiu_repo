from pyftdi.ftdi import Ftdi
import serial
import pyftdi.serialext
import random
import numpy as np

STX = b'\x02'
ETX = 0x03
ping = 0x70

print(STX)
baudrate = 115200

Ftdi.show_devices()
#ping_1 = b'\x02p09933DDC9AE1E1\x03'
#ping = b'\x02p5EA0547BFE2F2F\x03'
LED_1 = b'\x02\x0C5\x03'
version = b'\x02\x26\x03'
#
port = pyftdi.serialext.serial_for_url('ftdi://ftdi:ft-x:DK0HGAC5/1', baudrate=baudrate)
port.write(LED_1)
#data = port.read()
data=port.read_until(b'\x03')
print(data)
port.close()

#generate_unlock_bytes()
