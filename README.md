# qiu_repo


## WINDOWS

pyftdi needs to be setup with different driver. The Tool [Zadig](https://zadig.akeo.ie/) can be used to replace the FTDI driver to work with the pyftdi library.
Install the tool and click on **Options - List All Devices **. Select the needed FTDI devices and replace the driver with the **libusb-win32** driver.
After this the pyftdi can be used with python.
