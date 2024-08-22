from pyftdi.ftdi import Ftdi
import serial
import pyftdi.serialext
import random
import numpy as np

STX = 0x02
ETX = 0x03
ping = 0x70

baudrate = 115200

def generate_unlock_bytes():
    n1 = np.uint16(random.randrange(65000))
    b1 = np.uint8(n1 >> 8)
    b2 = np.uint8(n1)
    print(hex(b1))
    print(hex(b2))
    n2 = np.uint16(random.randrange(65000))
    b3 = np.uint8(n2 >> 8)
    b4 = np.uint8(n2)
    print(hex(b3))
    print(hex(b4))
    xor_1 = np.uint16((b1 << 8)+b3)
    xor_2 = np.uint16((b2 << 8)+b4)
    n3 = xor_1 ^  xor_2
    b5 = np.uint8(n3 >> 8)
    b6 = np.uint8(n3)
    byts = (b1,b2,b3,b4,b5,b6)
    print(hex(b1),hex(b2),hex(b3),hex(b4),hex(b5),hex(b6))
    unlock_string = bytearray(b'\x02')
    for b in byts:
        print(b)
        unlock_string.append(b)
    #unlock_string.append(b'\x03')
    print(unlock_string)
    return b1,b2,b3,b4,b5,b6
#def unlock_communication():


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
