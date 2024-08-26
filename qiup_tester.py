from pyftdi.ftdi import Ftdi
from Qiup import Qiup

qiup = Qiup(debug=False)

print("API Version")
qiup.get_api_version()
print("APPL Version")
qiup.get_appl_version()
print("Register")
qiup.register()
print("Release")
qiup.release()
