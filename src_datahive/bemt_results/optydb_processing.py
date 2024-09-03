import os
import pickle
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})

aoa_tab=[]
r_R_tab=[]

directory = r'C:\Users\jlari\Documents\GitHub\DSE-LARES-HIVE-Resources\src_datahive\bemt_results\SECTION_PROP_001'

def make_cplplot(cp_dict):
    counter_row = 0
    counter_column = 0

    fig, axs = plt.subplots(3, 3)
    for key in cp_dict.keys():
        axs[counter_row,counter_column].scatter(cp_dict[key]['x/c'], cp_dict[key]['CP'], color='#00a390')
        title_name = ''.join(['CP @', str(np.round(float(key),2))])
        axs[counter_row, counter_column].set_title(title_name)

        print('Currently filling in position:', counter_row, counter_column)
        counter_column+=1
        if counter_column==3:
            counter_column=0
            counter_row+=1
        else:
            continue
    for ax in axs.flat:
        ax.set(xlabel='x/c', ylabel='Cp')
    fig.tight_layout()
    return plt.show()

#open a file and check its content
#file = '\\'.join([directory, 'blade_in_pfr_cp_001.txt'])

cp = {}
read_data = False
if read_data:
    for file in os.listdir(directory):
        filename='\\'.join([directory,file])

        #get the angle of attack per radial section
        open_file_foraoa=open(filename)
        lines=open_file_foraoa.readlines()
        open_file_foraoa.close()
        for i in range(len(lines)):
            if i==3:
                r_R=lines[i][3:14]
                actual_r_R="{:.8f}".format(float(r_R))
                aoa=lines[i][42:53]
                actual_aoa="{:.8f}".format(float(aoa))

        r_R_tab.append(actual_r_R)
        aoa_tab.append(actual_aoa)

        #get the cp data (that you need to now store somewhere with a way to identify what belongs to what
        cp_data = pd.read_fwf(filename, skiprows=5, index_col=False, names=['x/c', '-cp', 'delta*/c', 'theta/c', 'Cf', 'BC'])
        cp_data.drop(['delta*/c', 'theta/c', 'Cf', 'BC'], inplace=True, axis=1)
        cp[str(actual_r_R)] = {}
        cp[str(actual_r_R)]['x/c'] = cp_data['x/c']
        cp[str(actual_r_R)]['CP'] = cp_data['-cp']

#save the data to make the code faster later
    save_cp_file = open('CP_data.pkl', 'wb')
    pickle.dump(cp, save_cp_file)
    save_cp_file.close()
    with open('r_R_list', 'wb') as save_r_R:
        savelist = pickle.dump(r_R_tab,save_r_R)
    with open('aoa_list', 'wb') as save_aoa:
        saveaoa = pickle.dump(aoa_tab,save_aoa)

if not read_data:
    with open('CP_data.pkl', 'rb') as save_cp_file:
        cp_dict = pickle.load(save_cp_file)
    with open('r_R_list', 'rb') as save_r_R:
        r_R = pickle.load(save_r_R)
    with open('aoa_list', 'rb') as save_aoa:
        aoa = pickle.load(save_aoa)

aoa = [float(i) for i in aoa]
aoa = np.round(aoa,2)
r_R = [float(j) for j in r_R]
r_R = np.round(r_R,2)

#aoa plot
plt.scatter(r_R,aoa, color='#00A6D6', marker='x')
plt.title('Sequence of angles of attack along the blade')
plt.xlabel('$r/R [-]$')
plt.ylabel('AoA [deg]')
plt.grid()
plt.show()

#CP plot
counter = 0
cp_9 = {}
cp_18 = {}
cp_27 = {}
cp_36 = {}
cp_45 = {}
cp_54 = {}

for key in cp_dict.keys():
    cp_dict[key]['x/c'] = [float(k) for k in cp_dict[key]['x/c']]
    cp_dict[key]['x/c'] = np.round(cp_dict[key]['x/c'],2)
    cp_dict[key]['CP'] = [float(l) for l in cp_dict[key]['CP']]
    cp_dict[key]['CP'] = np.round(cp_dict[key]['CP'],2)


    if counter<9:
        cp_9[key] = {}
        cp_9[key]['x/c'] = cp_dict[key]['x/c']
        cp_9[key]['CP'] = cp_dict[key]['CP']

    elif counter<18:
        cp_18[key] = {}
        cp_18[key]['x/c'] = cp_dict[key]['x/c']
        cp_18[key]['CP'] = cp_dict[key]['CP']

    elif counter<27:
        cp_27[key] = {}
        cp_27[key]['x/c'] = cp_dict[key]['x/c']
        cp_27[key]['CP'] = cp_dict[key]['CP']

    elif counter<36:
        cp_36[key] = {}
        cp_36[key]['x/c'] = cp_dict[key]['x/c']
        cp_36[key]['CP'] = cp_dict[key]['CP']

    elif counter<45:
        cp_45[key] = {}
        cp_45[key]['x/c'] = cp_dict[key]['x/c']
        cp_45[key]['CP'] = cp_dict[key]['CP']

    elif counter<54:
        cp_54[key] = {}
        cp_54[key]['x/c'] = cp_dict[key]['x/c']
        cp_54[key]['CP'] = cp_dict[key]['CP']

    else:
        continue

    counter += 1

#make a plot attempt
plot_0 = make_cplplot(cp_9)
plot_1 = make_cplplot(cp_18)
plot_2 = make_cplplot(cp_27)
plot_3 = make_cplplot(cp_36)
plot_4 = make_cplplot(cp_45)
plot_5 = make_cplplot(cp_54)