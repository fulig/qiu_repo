import numpy as np
import matplotlib.pyplot as plt
import re

with open("data_save", "r") as file:
    lines  = file.readlines()

#def plot_all_data(data):
#    fig,ax  =plt.subplots(len(data))
#    for i in len(data):
#        x = np.linspace(0,len(data[i])-1,len(data[i]) )
#        ax[i].plot(x, data[i])
#    plt.show()

fig, ax = plt.subplots(2)

data = []
swapped = []
for d in lines:
    line = d.rstrip().replace(" ", "")
    length = int(line[0:2], 16)
    data_line = line
    #print(data_line)
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

x = np.linspace(0,len(data)-1, len(data))
ax[0].plot(x,data)

data = []
for d in lines:
    line = d.rstrip().replace(" ", "")
    length = int(line[0:2], 16)
    data_line = line
    #print(data_line)
    swap_line = ""
    if (len(data_line)>64):
        print("-------------")
        print(data_line)
        data_line= re.sub("ff0[a-fA-F0-9]{3}","", data_line)
        #print(finds)
        #data_line = data_line.replace("ff", "")
        print(data_line)
        print("-------------")
    for i in range(int(len(data_line)/4)):
        b_data = data_line[i*4:(i+1)*4]
        #print(b_data)
        swap = b_data[2:] + b_data[:2]
        #print(swap)
        conv_data = int(swap, 16)& 0x0FFF
        #print(conv_data)
        data.append(conv_data)
        swap_line += swap

x = np.linspace(0,len(data)-1, len(data))
ax[1].plot(x,data)

plt.show()








