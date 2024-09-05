from Qiup import *
import numpy as np
import matplotlib.pyplot as plt
import struct

qiup = Qiup(debug=True)


data_list = []
qiup.setup_serial()
qiup.get_api_version()
qiup.register()
qiup.control_irled_intern(1)
qiup.control_power(1, 5)
qiup.puls_measure_control(0,0,1,1)
for i in range(200):
    data = qiup.get_measurement_data().hex()
    print(data)
    if int(data[0:4], 16) == 34:
        data_list.append(data[4:])
seperat_data = []
qiup.puls_measure_control(0,0,0,0)
qiup.release()
converted = []
for data in data_list:
    print(data)
    for i in range(16):
        b_data = data[i*4:(i+1)*4]
        #print(b_data)
        swap = b_data[2:] + b_data[:2]
        right_value = int(swap, 16) & 0x0FFF
        #print(hex(right_value))
        #print(swap)
        #print(right_value)
        #print("-----")
        converted.append(right_value)


#convert = []
#for data in data_list:
#    for i in range(int(len(data)/4)):
#        data_raw = data[i*4+1:(i*4)+4]
#        data_single = int(data_raw,16)
#        convert.append(data_single)

#print(convert)

x = np.linspace(0, len(converted)-1, len(converted))
plt.plot(x, converted)
plt.show()