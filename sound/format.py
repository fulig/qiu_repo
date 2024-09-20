with open("Sound_4_confirmation.hex", "r") as file:
    lines = file.readlines()

data_lines_32 = []
for i in range(int(len(lines)/2)):
    data_lines_32.append(lines[i*2].strip() + lines[i*2+1].strip())

print(data_lines_32)
with open("sound_4.txt", "w") as file:
    for i in data_lines_32:
        file.write(i+ "\n")