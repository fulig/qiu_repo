import numpy as np
import matplotlib.pyplot as plt

with open("data_save", "r") as file:
    lines  = file.readlines()

data = []
swapped = []
for d in lines:
    line = d.rstrip()
    length = int(line[0:2], 16)
    data_line = line
    swap_line = ""
    for i in range(int(len(data_line)/4)):
        b_data = data_line[i*4:(i+1)*4]
        #print(b_data)
        swap = b_data[2:] + b_data[:2]
        #print(swap)
        conv_data = int(swap, 16)& 0x0FFF
        #print(conv_data)
        data.append(conv_data)
        swap_line += swap
    swapped.append(swap_line)
print(swapped)
with open("swapped_data", "w") as file:
    file.write('\n'.join(swapped))

with open("data_save_man_fix", "r") as file:
    lines  = file.readlines()

data_fix = []
for d in lines:
    line = d.rstrip()
    length = int(line[0:2], 16)
    data_line = line
    for i in range(int(len(data_line)/4)):
        b_data = data_line[i*4:(i+1)*4]
        #print(b_data)
        swap = b_data[2:] + b_data[:2]
        conv_data = int(swap, 16)& 0x0FFF
        print(conv_data)
        data_fix.append(conv_data)

with open("fix_2", "r") as file:
    lines  = file.readlines()

data_fix_2 = []
for d in lines:
    line = d.rstrip()
    length = int(line[0:2], 16)
    data_line = line
    #if len(line) == 64:
    for i in range(int(len(data_line)/4)):
        b_data = data_line[i*4:(i+1)*4]
        #print(b_data)
        swap = b_data[2:] + b_data[:2]
        #print(swap)
        data_fix_2.append(int(swap, 16)& 0x0FFF)
x_fix_2 = np.linspace(0, len(data_fix_2)-1, len(data_fix_2))
x_fix = np.linspace(0, len(data_fix)-1, len(data_fix))
x = np.linspace(0, len(data)-1, len(data))


fig,ax = plt.subplots(3)

ax[0].plot(x_fix, data_fix)
ax[0].set_title("Fixed")

ax[1].plot(x_fix_2, data_fix_2)

ax[2].plot(x, data)
plt.show()




