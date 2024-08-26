from pyftdi.ftdi import Ftdi
from Qiup import Qiup

qiup = Qiup(debug=True)

qiup.get_api_version()
qiup.get_appl_version()
qiup.register()
qiup.release()