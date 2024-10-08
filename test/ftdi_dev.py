from pyftdi.ftdi import Ftdi
import serial
import pyftdi.serialext
import random
import numpy as np

STX = b'\x02'
ETX = 0x03
ping = 0x70
baudrate = 115200
print(b'\x5B')

Ftdi.show_devices()
#ping_1 = b'\x02p09933DDC9AE1E1\x03'
#ping = b'\x02p5EA0547BFE2F2F\x03'
LED_1 = b'\x02\x0C6E\x03'
version = b'\x02\x26\x03'
REGISTER = b'\x02\x3200\x03'
RELEASE = b'\x02\x34\x03'
REJECT = b'\x02\x01\x03'
IRLED_EXT = b'\x02\x061\x03'
VOLTAGE_0=b'\x02\x5A\x0A\x03'
VOLTAGE_1=b'\x02\x5A\x01\x03'
VOLTAGE_2=b'\x02\x5A\x02\x03'

DIM_VOL= b'\x02\x0A5265\x03'
DIM_VOL = b'\x02\x0A\x35\x32\x36\x35\x03'
dim = bytearray(b'\x02\x0A')

rgb = "G"
value = 5
rgb_val = hex(ord(rgb))[2:]
print(rgb_val)
value = "{:02X}".format(value)
print(value)
numbers = rgb_val + value
print(numbers)
#numbers = "5265"
dim.extend(map(ord, numbers))
dim.extend(b'\x03')
print(dim)
power_led = bytearray(b'\x02\x5A\x30\x31\x30\x34\x03')
power_analog = bytearray(b'\x02\x5A\x30\x31\x30\x35\x03')

#url = "ftdi://ftdi:ft-x:DQ00QN2Q/1"
url = "ftdi://ftdi:ft-x:DK0HGAC5/1"
port = pyftdi.serialext.serial_for_url(url, baudrate=baudrate)
port.write(REGISTER)
data = port.read_until(b'\x03')
print(data)
port.write(power_led)
data=port.read_until(b'\x03')
print(data)
port.write(power_analog)
data=port.read_until(b'\x03')
print(data)
port.write(LED_1)
data = port.read_until(b'\x03')

#for i in range(255):
#    send_data = b'\x02' b'\x5A' + i.to_bytes(1) + b'\x03'
#    print(f"Send : {send_data}")
#    port.write(send_data)
#    rec_data = port.read_until(b'\x03').lstrip(b'\x02').rstrip(b'\x03')
#    print(rec_data)
    #print(f"Recv : {rec_data}")
    #if rec_data[0] != 55:
    #    print(send_data)
    #    print(rec_data)

#port.write(VOLTAGE_0)
#data = port.read()
#data=port.read_until(b'\x03')
#print(data)
#port.write(VOLTAGE_1)
#data = port.read()
#data=port.read_until(b'\x03')
#print(data)
#port.write(VOLTAGE_2)
#data = port.read()
#data=port.read_until(b'\x03')
#print(data)
#port.close()

#generate_unlock_bytes()
