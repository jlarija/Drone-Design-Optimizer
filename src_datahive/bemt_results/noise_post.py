import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import csv

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})

def mic_positions(x_init, x_fin, z_init, z_fin, plane):
    x = np.arange(x_init, x_fin, 0.1)
    z = np.arange(z_init, z_fin, 0.1)
    init_array = np.zeros((int((len(x)*len(z))),3))
    z = np.transpose(z)
    count=0

    if plane=='y':
        n1 = 2
        n2 = 0

    elif plane=='x':
        n1 = 2
        n2 = 1
    else:
        n1 = 0
        n2 = 1

    for k in range(len(x)):
        for n in range(len(z)):
            init_array[count][n1] = z[n] #you will have to change the index from 0,1,2 dpeending if it's xyz
            init_array[count][n2] = x[k]
            count+=1

    return np.round(init_array,2)

init = mic_positions(-0.4000,0.5000, -0.4000,0.5000,'y')

with open('mic_positions.txt', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=' ')
    for row in np.round(init,2):
        writer.writerow(row)
    f.close()

mic_loc = pd.read_fwf('mic_positions.txt', skiprows=1, index_col=False, names=['x', 'y', 'z'])
oaspl = pd.read_fwf('blade_in_pfr_bb_oaspl_APC.txt', skiprows=1, index_col=False, names=['Mic#', 'OASPL', 'OASPL-A','OASPL-D'])

blade_length = 0.3154

fig, ax = plt.subplots()
plt.scatter(x=init[:,0], y=init[:,2], c=oaspl['OASPL-A'], cmap='viridis',s=oaspl['OASPL-A']*5)
plt.vlines(-0.02, -blade_length, blade_length, color='black', label='Blade')
plt.hlines(blade_length, -0.02, 0.02, color='black')
plt.hlines(-blade_length, -0.02, 0.02, color='black')
plt.vlines(0.02, -blade_length, blade_length, color='black')
plt.xlabel('X [m]')
plt.ylabel('Z [m]')
plt.title('Noise map for constant y = 0')
cbar = plt.colorbar()
plt.legend()
plt.grid()
cbar.set_label('OASPL-A [dB]')
plt.show()

