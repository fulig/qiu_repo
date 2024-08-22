#!/bin/sh

if [ $1 = "set" ]; then
	cp ./11-ftdi.rules /etc/udev/rules.d/
fi
if [ $1 = "unset" ]; then
	rm /etc/udev/rules.d/11-ftdi.rules
fi
udevadm control --reload-rules
udevadm trigger
