from pyftdi.ftdi import Ftdi

BAUDRATES = (300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200,
             230400, 460800, 576000, 921600, 1000000, 1500000, 1843200,
             2000000, 2500000, 3000000, 4000000, 6000000, 8000000,
             12000000)


ftdi = Ftdi()
ftdi.open_from_url('ftdi://ftdi:232:BS0410/1')
for baudrate in BAUDRATES:
    actual, _, _ = ftdi._convert_baudrate(baudrate)
    ratio = baudrate/actual
    print(f"Baudrate: {baudrate} Ratio : {ratio}")