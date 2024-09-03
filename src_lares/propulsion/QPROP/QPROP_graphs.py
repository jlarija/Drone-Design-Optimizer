'''
Author: @jlarija
The aim of this code is to ge the propeller and motor files ready to be imported into QPROP. The motor file is
easy to create so can just be created in a txt, but the propeller files needs some twisting from the APC data.
'''
import os
import sys

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

sys.path.append('/home/jlarija/Desktop/PycharmProjects/OwnFiles')
import Pretty_Graphs

this_loc = os.getcwd()

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})


class MakeFiles:

    def __init__(self, blade_data, destination_data):
        self.blade_data = blade_data
        self.destination_data = destination_data
        return

    def get_propeller_geometry(self):

        airfoil_data = open(self.blade_data)
        lines = airfoil_data.readlines()
        airfoil_data.close()

        columns = []
        radial_station = []
        chord = []
        twist = []

        for line in lines:
            if len(line.strip()) > 0:
                columns_0 = line.split(" ")

                columns_1 = list(filter(None, columns_0))

                for i in range(len(columns_1)):
                    columns_1[i] = columns_1[i].strip()

                columns.append(columns_1)

        final_cols = columns[23:59]

        for m in range(len(final_cols)):
            radial_station.append(float(final_cols[m][0]))
            chord.append(float(final_cols[m][1]))
            twist.append(float(final_cols[m][7]))

        # convert to arrays and multiply to SI units
        radial_station = np.array(radial_station)
        chord = np.array(chord)
        twist = np.array(twist)

        return radial_station, chord, twist

    def write_onto_file(self, radial_section, chord, twist, airfoil):

        with open(self.destination_data, 'w', encoding='UTF8', newline='') as qprop_file:

            if airfoil == 'ClarkY':
                qprop_file.write(''.join([str(self.destination_data), '\n \n',
                                          '2   7 ! Nblades  [ R ] \n \n',
                                          '0.3674  6.5412   ! CL0     CL_a \n',
                                          ' -0.4964  1.3694   ! CLmin   CLmax \n \n',
                                          '0.01875  0.038  0.0058 0.7926   !  CD0    CD2u   CD2l   CLCD0 \n',
                                          '100000   -0.7              !  REref  REexp \n \n',
                                          '0.0254  0.0254   1.0  !  Rfac   Cfac   Bfac  \n',
                                          '0.      0.       0.   !  Radd   Cadd   Badd  \n \n',
                                          '#  r    chord    beta\n']))

            elif airfoil == 'NACA4412':
                qprop_file.write(''.join([str(self.destination_data), '\n \n',
                                          '2   7 ! Nblades  [ R ] \n \n',
                                          '0.4455  6.76  ! CL0     CL_a \n',
                                          ' -0.35  1.37   ! CLmin   CLmax \n \n',
                                          '0.0174  0.012  0.0025 0.5651   !  CD0    CD2u   CD2l   CLCD0 \n',
                                          '100000   -0.5              !  REref  REexp \n \n',
                                          '0.0254  0.0254   1.0  !  Rfac   Cfac   Bfac  \n',
                                          '0.      0.       0.   !  Radd   Cadd   Badd  \n \n',
                                          '#  r    chord    beta\n']))

            else:
                print('Please input an airfoil. Supported modes for now: NACA4412 or ClarkY')

            for n in range(len(radial_section)):
                qprop_file.write(''.join([str(radial_section[n]), '   ', str(chord[n]), '   ', str(twist[n]), '\n']))

        return 'File written'


def read_output_file(filetoread, cols_start, cols_stop):
    airfoil_data = open(filetoread)
    lines = airfoil_data.readlines()
    airfoil_data.close()

    columns = []

    rpm = []
    thrust = []
    volts = []
    power = []
    amps = []

    for line in lines:
        if len(line.strip()) > 0:
            columns_0 = line.split(" ")

            columns_1 = list(filter(None, columns_0))

            for i in range(len(columns_1)):
                columns_1[i] = columns_1[i].strip()

            columns.append(columns_1)

    final_cols = columns[cols_start:cols_stop]  # added this to account for different files dimensions.

    for m in range(len(final_cols)):
        rpm.append(float(final_cols[m][1]))
        thrust.append(float(final_cols[m][3]))
        power.append(float(final_cols[m][5]))
        volts.append(float(final_cols[m][6]))
        amps.append(float(final_cols[m][7]))

    # convert to arrays and multiply to SI units, and make a
    rpm = np.array(rpm)
    thrust = np.array(thrust) - 0.05 * np.array(thrust)
    power = np.array(power)
    volts = np.array(volts)
    amps = np.array(amps)

    return rpm, thrust, power, volts, amps


def scatter_darkbackground_doubleplot(x_data_1, y_data_1, xlabel_1, ylabel_1, title, color,
                                      x_data_2, y_data_2, xlabel_2, ylabel_2, color_2,
                                      y_data_3, third_label, color_3):
    sns.set(style="darkgrid", context="talk")
    plt.style.use("dark_background")

    fig, axes = plt.subplots(2, 1, figsize=(9, 9))

    fig.suptitle(str(title))

    # plot 1
    sns.scatterplot(ax=axes[0], x=x_data_1, y=y_data_1, color=str(color), legend=False)
    axes[0].set(xlabel=str(xlabel_1), ylabel=str(ylabel_1))
    axes[0].axhspan(32, 130, facecolor='#99d28c', alpha=0.5, label='Exceeds required thrust for T/W = 1.4')
    axes[0].axvspan(7500, 15000, facecolor='#82d7c6', alpha=0.5, label='RPM limit prescribed by APC')
    axes[0].tick_params(grid_linestyle=':')
    axes[0].set_xlim(0, 15000)
    axes[0].set_ylim(-2, 100)
    axes[0].grid(which='both', alpha=0.5)
    axes[0].legend(loc='upper left')

    # plot 2

    sns.scatterplot(ax=axes[1], x=x_data_2, y=y_data_2, color=str(color_2))
    axes[1].axvspan(32, 150, facecolor='#82d7c6', alpha=0.5, label='Exceeds required thrust for T/W = 1.4')
    axes[1].set_xlabel(str(xlabel_2))
    axes[1].set_ylabel(str(ylabel_2), color=str(color_2))
    axes[1].tick_params(grid_linestyle=':', axis='y', labelcolor=color_2)

    third_axis = axes[1].twinx()
    sns.scatterplot(ax=third_axis, x=x_data_2, y=y_data_3, color=str(color_3))
    third_axis.axhspan(75, 200, facecolor='#99d28c', alpha=0.5, label='Current Limit')
    third_axis.tick_params(axis='y', labelcolor=str(color_3))
    third_axis.grid(visible=None)
    third_axis.set_ylabel(str(third_label), color=str(color_3))

    third_axis.legend(loc='upper left')
    lines, labels = axes[1].get_legend_handles_labels()
    lines2, labels2 = third_axis.get_legend_handles_labels()

    third_axis.legend(lines + lines2, labels + labels2, loc='lower right')
    axes[1].grid(which='both', alpha=0.5)
    axes[1].tick_params(grid_linestyle=':')

    plt.xlim(0, 150)
    axes[1].set_ylim(0, 1800)
    third_axis.set_ylim(0, 100)
    plt.tight_layout()

    return plt.show()


# Statements to decide what to do with the code
create_qprop_file = False
read_data = True
graphing = True

if create_qprop_file == True:
    file = '/src_lares/propulsion/QPROP/Propeller Geometries/apc14x55MR_formAPC.txt'

    prop = MakeFiles(file,
                     '/home/jlarija/Desktop/PycharmProjects/DSE-LARES-HIVE-Resources/src_lares/propulsion/QPROP/Propeller Geometries/apc14x55MR_NACA4412_QPROPformat.txt')
    prop.write_onto_file(prop.get_propeller_geometry()[0], prop.get_propeller_geometry()[1],
                         prop.get_propeller_geometry()[2], 'NACA4412')

if read_data == True:
    filename = 'apc14x55MR_NACA4412_AT4130KV450.txt'

    file_to_read = ''.join([str(this_loc), '/Propellers coupled to Motors/', str(filename)])

    data = read_output_file(file_to_read, 16, 32)

if graphing == True:
    plot_APC14 = scatter_darkbackground_doubleplot(data[0], data[1], 'RPM [-]', 'Thrust [N] ',
                                                   'AT4130KV450 + APC14x5.5MR - NACA4412',
                                                   Pretty_Graphs.TUDelft_colors()[0],
                                                   data[1], data[2], 'Thrust [N]', 'Power [W]', '#AA4499',
                                                   data[4], 'Current [A]', '#DDCC77')
