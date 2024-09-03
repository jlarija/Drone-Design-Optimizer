import csv
import os

directory = r'C:\Users\jlari\Documents\GitHub\DSE-LARES-HIVE-Resources\src_lares\propulsion\rotor\CRotor' \
            r'\CRotor755es13_win32\bin\04 cad_blades'

command_1 = ['StartLoft']
command_2 = ['StartCurve']
command_3 = ['EndCurve']
command_4 = ['EndLoft']
command_5 = ['End']

columns = []
columns.append(command_1)

for file in os.listdir(directory):
    name_file = '\\'.join([directory, file])
    current_file = open(name_file)
    lines = current_file.readlines()
    current_file.close()

    columns.append(command_2)

    for line in lines:
        if len(line.strip()) > 0:
            columns_0 = line.split(" ")

            columns_1 = list(filter(None, columns_0))

            for i in range(len(columns_1)):
                columns_1[i] = columns_1[i].strip()
                columns_1[i] = float(columns_1[i]) * 10 ** (3)

            columns.append(columns_1)

    columns.append(command_3)

columns.append(command_3)
columns.append(command_4)
columns.append(command_5)

write_data = True

if write_data:
    with open('esprop.csv','w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(columns)



