with open("audio0.txt", "r") as file:
    lines = file.readlines()

clean_lines = []
for line in lines:
    clean_lines.append(line.strip().replace("0x", ""). replace(',', ''))
data_lines_32 = []
print(clean_lines)
for i in range(int(len(clean_lines)/2)):
    data_lines_32.append(clean_lines[i*2] + clean_lines[i*2+1])

print(data_lines_32)
with open("audio0_32.txt", "w") as file:
    for i in data_lines_32:
        file.write(i+ "\n")