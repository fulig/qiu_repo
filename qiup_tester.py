from pyftdi.ftdi import Ftdi
from Qiup import Qiup
import time

qiup = Qiup(debug=False)


#print("API Version")
#qiup.get_api_version()
#print("APPL Version")
#qiup.get_appl_version()
print("Register")
qiup.register(0)
qiup.get_voltage(0)
qiup.get_voltage(1)
qiup.get_voltage(2)
qiup.get_voltage(3)
qiup.dim_led("R", 65)
qiup.dim_led("G", 65)
#qiup.control_power(1, 0)
#qiup.get_charge_state()
#qiup.control_irled_ext(0)
#qiup.control_irled_ext(1)
#qiup.control_irled_intern(1)
#print("Wait")
#time.sleep(14)
#print("Retrigger")
#qiup.register_retrigger()
#print("Release")
#qiup.release()
#qiup._trigger_reject()
#print(hex(ord("G")))