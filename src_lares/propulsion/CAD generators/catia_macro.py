#the idea is to take the macro in CATIA and automate it for every section

#write command in a txt
import numpy as np

spline_file = 'spline only.txt'

n_int = 119
point_start = 3841
point_end = 5760

file = open(spline_file)
lines = file.readlines()
file.close()
line_start = 11

#somehow make the loop different for the first and last - so some inner loop construction that keeps the lines somewhere
# (if you append the lines first and make a copy it works)
get_loops = np.round(((point_end - point_start) / n_int), 0)
for i in range(len(get_loops)):

'''
for i in range(len(lines)):
    while '\n' in lines:
        lines.remove('\n') #clear up empty lines to save space on final file

    if i == line_start and line_start < 368:
        try:
            point_value = lines[line_start][-7:-3]
            current_line = lines[line_start]
            lines[i] = current_line.replace(point_value, str(point_start))

            point_start += 1
            line_start += 3
        except IndexError:
            pass

write_data = False

if write_data: 
    with open('macro1.txt', 'w') as file:
        file.writelines(lines)
        file.close()

#now this works; the same text can be used to the subsequent points
'''





