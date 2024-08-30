from pyftdi.ftdi import Ftdi
from Qiup import Qiup
import time
from voltages import *

qiup = Qiup(debug=False)
#qiup = Qiup(debug=True)


#print("API Version")
#qiup.get_api_version()
#print("APPL Version")
#qiup.get_appl_version()
print("Register")
if qiup.register(0) == 1:
    print("Already registered. Releasing..")
    qiup.release()
    print("Retry register..")
    qiup.register(0)
#time.sleep(1)
#qiup.register_retrigger()
qiup.control_power(1,QP_API_LED_SUPPLY_VOLTAGE)
qiup.control_power(1,QP_API_ANALOG_SUPPLY_VOLTAGE)
#qiup.control_power(0,QP_API_LED_SUPPLY_VOLTAGE)
#qiup.control_power(0,QP_API_ANALOG_SUPPLY_VOLTAGE)

#qiup.get_voltage(QP_API_ACCU_VOLTAGE)
#qiup.get_voltage(QP_API_USB_VOLTAGE)
#qiup.get_voltage(QP_API_DIG_SUPPLY_VOLTAGE)
#qiup.get_voltage(10)

#qiup.get_charge_state() # --> Takes longer to request..???

#qiup.control_irled_ext(0)
#qiup.control_irled_ext(1)

#qiup.control_irled_intern(1)
#qiup.control_irled_intern(0)
#qiup.dim_led('R', 0)
#qiup.dim_led('G', 0)
#qiup.dim_led('B', 0)
#while True:
#    for i in range(65):
#        qiup.dim_led('B', i)
#        time.sleep(2/(65))
#    for i in range(65):
#        qiup.dim_led('B', 65-i)
#        time.sleep(2/(65))

#data = "1234567812345678123456781234567812345678123456781234567812345678"
#qiup.stop_measure()
#qiup.ledbar_control([0,0,0,0,1,1,0,0])
#qiup.check_earclip()
#print("Erase flash")
#qiup.erase_flash(8112)
#print("Read flash")
#qiup.read_flash(8112, 3)
#print("write flash")
#qiup.write_flash(8112, 3, data)
#print("read flash")
#qiup.read_flash(8112, 3)
#print("PULS_MEASURE start")
#qiup.puls_measure_control(0,0,1,1)
#time.sleep(0.5)
#qiup.puls_measure_control(0,0,0,0)

#qiup.set_gain(0)
#qiup.get_gain()
#qiup.set_gain(1)
#qiup.get_gain()
#qiup.set_gain(2)
#qiup.get_gain()
#qiup.set_gain(3)
#qiup.get_gain()
#print("Gain")
#qiup.get_gain()

#qiup.get_datetime()
#qiup.set_datetime([2024,9,12,13,12,11])
#qiup.get_datetime()
qiup.set_time_from_pc()
#qiup.get_datetime()

#qiup.play_sound(0)
#time.sleep(1)
#qiup.play_sound(1)
#time.sleep(1)
#qiup.play_sound(2)
#time.sleep(1)
#qiup.play_sound(3)
#time.sleep(1)
#qiup.play_sound(4)
#time.sleep(1)
#qiup.play_sound(5)

#qiup.pushbutton_state()

qiup.get_accel()

qiup.get_event_vector()
#qiup.write_flash(44, 44, 1, data)
#qiup.erase_flash(4444)
#qiup.read_flash(4444, 1)
#print("EARCLIP") 
#qiup.check_earclip()

#qiup.ledbar_control(0)
#
#qiup.ledbar_control(4)
#print("LED bar 8 ")
#qiup.ledbar_control(32)
#qiup.release()
#qiup.get_charge_state()
#qiup.get_voltage(0)
#qiup.get_voltage(1)
#qiup.get_voltage(2)
#qiup.get_voltage(3)
#qiup.dim_led("R", 65)
#qiup.dim_led("G", 65)
#qiup.control_power(1, 0)
#qiup.get_charge_state()
